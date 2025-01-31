# OOP25_Notebook

## Prerequisites

### Clone repo with https
Install [git](https://git-scm.com/downloads) if you don't already have it, then: 

`git clone https://github.com/hiqs-gmbh/OOP25_Notebook.git`. 


### Docker Compose
Install [Docker Desktop](https://docs.docker.com/compose/install/) if you don't already have it, then: 
Start the Docker Compose file ```docker-compose.yml``` (outside the Dev Container)


### Dev Container Extension 
Install [Visual Studio Code](https://code.visualstudio.com/download) if you don't already have it, then install Dev Container Extension: 

![alt text](./imgs/extension.png)

### Startup Dev Container
**Click button at the bottom left of VSCode**

![alt text](./imgs/dev_cont_button.png)

**Open current folder in Dev Container**

![alt text](./imgs/open_folder_in_cont.png)


## Hugging Face Token
A [Hugging Face Token](https://huggingface.co/settings/tokens) is required to be able to download the Pyannote AI model.

Create an account first on [https://huggingface.co/join](https://huggingface.co/join).

Then go to Settings and Tokens and generate an Access Token. Then add this to the .env under ```PYANNOTE_HF_TOKEN```. 

If you wish, you can restrict the rights of your token (when selecting the ```Fine Grained``` type) to the following repositories.

![alt text](./imgs/hf_repo.png)


## Erste Schritte im Container
run download-model.ipynb
kopiere .env.example in neue .env
