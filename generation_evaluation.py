'''
This code is used to evaluate the FID score of the generated images.
You should at least guarantee this code can run without any error on test set.
And whether this code can run is the most important factor for grading.
We provide the remaining code,  you can't modify the remaining code, all you should do are:
1. Modify the sample function to get the generated images from the model and ensure the generated images are saved to the gen_data_dir(line 12-18)
2. Modify how you call your sample function(line 31)
'''
from pytorch_fid.fid_score import calculate_fid_given_paths
from utils import *
from model import * 
from dataset import *
import os
import torch
# You should modify this sample function to get the generated images from your model
# This function should save the generated images to the gen_data_dir, which is fixed as 'samples'
# Begin of your code
sample_op = lambda x : sample_from_discretized_mix_logistic(x, 5)
def my_sample(model, gen_data_dir, device, sample_batch_size=25, obs=(3,32,32)):
    model.eval()  
    for label in my_bidict:
        print(f"Label: {label}")
        labels = torch.full((sample_batch_size,), my_bidict[label], dtype=torch.long, device=device)
        input_tensor = torch.zeros(sample_batch_size, *obs, device=device)
        with torch.no_grad():
            output = model(input_tensor, labels=labels, sample=True)
            images = sample_from_discretized_mix_logistic(output, 5)  
            images = rescaling_inv(images)   
            save_images(images, gen_data_dir, label=label)

if __name__ == "__main__":
    ref_data_dir = "data/test"
    gen_data_dir = "samples"
    BATCH_SIZE=128
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    if not os.path.exists(gen_data_dir):
        os.makedirs(gen_data_dir)
    #Begin of your code
    #Load your model and generate images in the gen_data_dir
    model = PixelCNN(nr_resnet=1, nr_filters=40, input_channels=3, nr_logistic_mix=5)
    model_path = 'conditional_pixelcnn.pth'
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model = model.eval()
    my_sample(model=model, gen_data_dir=gen_data_dir, device=device)
    #End of your code
    paths = [gen_data_dir, ref_data_dir]
    print("#generated images: {:d}, #reference images: {:d}".format(
        len(os.listdir(gen_data_dir)), len(os.listdir(ref_data_dir))))

    try:
        fid_score = calculate_fid_given_paths(paths, BATCH_SIZE, device, dims=192)
        print("Dimension {:d} works! fid score: {}".format(192, fid_score, gen_data_dir))
    except:
        print("Dimension {:d} fails!".format(192))
        
    print("Average fid score: {}".format(fid_score))
