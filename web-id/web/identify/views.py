from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.files.images import ImageFile, File
from django.core.files.storage import default_storage
from . import aligndata_first as a
from . import create_classifier_se as c
from . import face_detection,const
from scipy import spatial
import numpy as np
import os
# Create your views here.
def index(request):
    return render(request,'identify/login.html')

def register(request):
    if request.method =='POST':
        print(request.FILES)
        id = request.POST['id']
        video_data = request.FILES['video-train']
        video = ImageFile(video_data)
        video_name = request.POST['video-filename']
        video_path = 'video/' + str(id) + "/" + video_name
        if default_storage.exists(video_path):
            default_storage.delete(video_path)
        default_storage.save(video_path, video)
        number_of_faces = face_detection.face_detect(id)
        a.align(const.FACE_TRAIN_FOLDER+"/"+str(id), "output_dir/"+str(id))
        emb_array, max_dist = c.getEmbeddingVectors("output_dir/"+str(id))
        np.savetxt(str(id)+".csv", emb_array, delimiter=",")
        f  = open(str(id)+'.txt','w')
        f.write(str(max_dist))
    return render(request,'identify/register.html')
   
def login(request):
    if request.method =='POST':
        print(request.FILES)
        id = request.POST['id']
        video_data = request.FILES['image']
        video = ImageFile(video_data)
        video_name = request.POST['id']
        video_path = 'image/' + str(id) + "/" + video_name
        if default_storage.exists(video_path):
            default_storage.delete(video_path)
        default_storage.save(video_path, video)
        a.align(const.TMP_FOLDER + str(id), "test_output/"+str(id))
        emb_vecto, max_dist= c.getEmbeddingVectors("test_output/"+str(id))   
        emb_array = np.loadtxt(str(id)+".csv",delimiter=",")
        test = np.max(spatial.distance.cdist(emb_array,emb_vecto ,metric='cosine'))
        f_name = os.listdir(const.BASE_DIR + '/test_output/'+str(id))[0]
        file_path= os.path.join(const.BASE_DIR+ '/test_output/'+str(id),f_name)
        os.remove(file_path)
        f = open(str(id)+'.txt','r')
        max_dist = float(f.read())
        if(test<max_dist):
            respone = {
            'message': 'Login successful'
            }
            return JsonResponse(respone)
        else:
            respone = {
            'message': 'Failed'
            }
            return JsonResponse(respone)
    return render(request,'identify/login.html')
    
