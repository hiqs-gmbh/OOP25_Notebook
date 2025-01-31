
import torch
import json
import os
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from dotenv import load_dotenv
from pyannote.audio import Pipeline

def run_whisper(audio_path: str):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    # Modell-ID von Whisper
    # model_id = "openai/whisper-large-v3-turbo"
    model_id = "openai/whisper-base"

    # Modell laden
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, 
        torch_dtype=torch_dtype, 
        low_cpu_mem_usage=True, 
        use_safetensors=True,
    )
    model.to(device)

    # Prozessor laden
    processor = AutoProcessor.from_pretrained(model_id)

    # Forced Decoder IDs für Deutsch (Transkription)
    forced_decoder_ids = processor.get_decoder_prompt_ids(language="de", task="transcribe")

    # Pipeline einrichten
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
        return_timestamps=True,
    )

    result = pipe(audio_path, generate_kwargs={"forced_decoder_ids": forced_decoder_ids})
    
    return result


def run_pyannote(hf_token: str, model: str, audio_path: str):
    # Laden der Diarization-Pipeline
    pipeline = Pipeline.from_pretrained(
        model,
        use_auth_token=hf_token
    )

    # Audio verarbeiten
    diarization = pipeline(audio_path)

    # Ergebnisse in strukturierter Form sammeln
    diarization_data = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        diarization_data.append({
            "start": turn.start,
            "end": turn.end,
            "speaker": speaker
        })

    return diarization_data

def run_matching(whisper_data, pyannote_data):
    # Liste für die zusammengeführten Ergebnisse
    merged_output = []

    # Durch alle Whisper-Chunks iterieren
    for chunk in whisper_data["chunks"]:
        chunk_start = chunk["timestamp"][0]
        chunk_end = chunk["timestamp"][1]
        chunk_text = chunk["text"]

        # Standard-Sprecher = "Unknown"
        speaker = "Unknown"

        # Überprüfe, ob dieses Chunk mit einem Diarization-Segment übereinstimmt
        for segment in pyannote_data:
            if chunk_start >= segment["start"] and chunk_end <= segment["end"]:
                # Das Whisper-Chunk liegt komplett in diesem Segment
                speaker = segment["speaker"]
                break
            elif chunk_start <= segment["end"] and chunk_end >= segment["start"]:
                # Teil-Überlappung
                speaker = segment["speaker"]
                break

        if speaker == "Unknown":
            print(f"Warning: No speaker found for chunk '{chunk_text}' [{chunk_start:.2f}s to {chunk_end:.2f}s]")

        merged_output.append({
            "speaker": speaker,
            "text": chunk_text.strip(),
            "start": chunk_start,
            "end": chunk_end
        })

    return merged_output