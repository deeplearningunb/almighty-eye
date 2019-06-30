## Almighty-Eye
### Python3 and openCV 
A facial recognition system.  The system is capable of recognizing faces in a live video stream, and to identify pre-trained faces.

### Setting up environment with Anaconda
  1. Install [`Anaconda`](https://docs.conda.io/en/latest/) to do this.
  2. Create `Almighty-eye` environment. Run on terminal:  
      ```conda create -n your_env_name python=3.6```
  3. Activate the environment with:  
    ```conda activate your_env_name```  
  5. Install the necessary libraries. Into the folder of the project, run:  
    ```pip install -r requirements.txt```
  6. Install openCV through conda command:  
    ```conda install -c conda-forge opencv```
  7. Install pillow through conda command:
    ```conda install -c conda pillow```
  
	
## Create a dataset directory
1. Inside the `sys/` directory, create a `dataset/` folder.
2. In the `dataset/` directory create folders with the name of the person to be identified
	
	
## Run programq
1. Run in the terminal with the virtual environment activate: `python3 main.py`
2. In the camera open, press `q` to exit program
	
	
## Training a new model model
1. Create a folder inside dataset with the name of the person.
2. Put pictures of her face inside the folder.
3. Run `model.py` file to training the model.
4. Run `main.py` to start the recognition
*note: we recommend you to get at least 20 images on each dataset
	
## References
1.  Image search engines tutorials [`PyImageSearch`](https://www.pyimagesearch.com/).
2.  [`FaceNet: A Unified Embeddings for Face Recognition and Clustering`](https://www.cv-foundation.org/openaccess/content_cvpr_2015/app/1A_089.pdf)
3. The database used to train the Not Recognized persons [`allfaces`](https://cswww.essex.ac.uk/mv/allfaces/index.html)

	

	
	

