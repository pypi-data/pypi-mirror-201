from nwebclient import sdb
from nwebclient import ticker
import json
import os
import requests
import time

from diffusers import PNDMScheduler, DDIMScheduler, LMSDiscreteScheduler, EulerDiscreteScheduler, DPMSolverMultistepScheduler
import torch
from diffusers import StableDiffusionPipeline

def gen(pipe, prompt='photo', negative_prompt = None, prefix='sd',  guidance_scale = 7.5, num_inference_steps=30, height=800, width=640, num_images=1, dbfile='data.db'):
    # https://huggingface.co/docs/diffusers/v0.14.0/en/api/pipelines/stable_diffusion/text2img#diffusers.StableDiffusionPipeline.__call__
    images = pipe(
      prompt,
      height = 800,
      width = 640,
      num_inference_steps = num_inference_steps,      # higher better quali default=45
      guidance_scale = guidance_scale,                # Prioritize creativity  7.5  Prioritize prompt (higher)
      num_images_per_prompt = num_images,
      negative_prompt = negative_prompt,
      ).images
    for i in range(len(images)):
        #  images[i].save(prefix+str(i)+".jpg")
        sdb.sdb_write_pil(images[i], prompt, negative_prompt, guidance_scale, prefix, dbfile)


"""
  ig = ImageGen()
  ig.prompt = "photo"
  ig.loop(5)
  
  ig.executeFromUrl('https://...')
"""
class ImageGen:
    # scheduler
    pipe = None
    prompt = "photo"
    negative_prompt = "text, cartoon, anime, drawing, meme, postcard, painting, ((fuzzy)), ((blurred)), ((low resolution)), ((b&w)), ((monochrome)), ambiguous, ((deformed)), oversaturated, ((out of shot)), ((incoherent)), (((glitched))), (((3d render))), cgi, ((incorrect anatomy)), bad hands, lowres, long body, ((blurry)), double, ((duplicate body parts)), (disfigured), (extra limbs), fused fingers, extra fingers, malformed hands, ((((mutated hands and fingers)))), conjoined, ((missing limbs)), logo, signature, mutated, jpeg artifacts, low quality, bad eyes, oversized, disproportionate, (((incorrect proportions))), exaggerated, (((aliasing)))"
    guidance_scale = 7.5
    num_inference_steps=25
    height=800
    width=640
    num_images=1
    prefix = 'sd'
    dbfile='data.db'
    # sdb jpg
    save_mode='sdb'
    loaded_model = None
    gen_count = 0
    def __init__(self, model_id="XpucT/Deliberate"):
        self.model_id = model_id
    def load(self):
        if self.loaded_model == self.model_id:
            return
        self.scheduler = DPMSolverMultistepScheduler.from_pretrained(self.model_id, subfolder="scheduler")
        device = "cuda"
        model_revision = None
        if self.scheduler is None:
           self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, torch_dtype=torch.float16, revision=model_revision)
        else:
           self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, scheduler=self.scheduler, custom_pipeline="lpw_stable_diffusion", torch_dtype=torch.float16, revision=model_revision)
        self.pipe = self.pipe.to(device)
        if self.model_id=="XpucT/Deliberate" or self.model_id == "SG161222/Realistic_Vision_V1.4_Fantasy.ai":
            self.pipe.safety_checker = lambda images, clip_input: (images, False)
        self.load_model = self.model_id
    def gen(self, loop_number=1):
        if self.pipe is None:
            self.load()
        images = self.pipe(self.prompt,
            height = self.height,
            width = self.width,
            num_inference_steps = self.num_inference_steps,      # higher better quali default=45
            guidance_scale = self.guidance_scale,                # Prioritize creativity  7.5  Prioritize prompt (higher)
            num_images_per_prompt = self.num_images,
            negative_prompt = self.negative_prompt,
        ).images
        self.gen_count = self.gen_count + 1
        for i in range(len(images)):
            #  images[i].save(prefix+str(i)+".jpg")
            self.save_image(images[i], i, loop_number)
    def save_image(self, image, i, loop_number):
        if self.save_mode == 'sdb':
            sdb.sdb_write_pil(image, self.prompt, self.negative_prompt, self.guidance_scale, self.prefix, self.dbfile)
        if self.save_mode == 'jpg':
            image.save(self.prefix+'_'+str(loop_number)+'_'+str(i)+'.jpg')
    def loop(self, count):
        for i in range(count):
            print("Loop "+str(i)+"/"+str(count))
            self.gen(loop_number=i)
    def execute(self, data):
        if "prompt" in data:
            self.prompt = data['prompt']
        if "negative_prompt" in data:
            self.negative_prompt = data['negative_prompt']
        if "prefix" in data:
            self.prefix = data['prefix']
        if "guidance_scale" in data:
            self.guidance_scale = float(data['guidance_scale'])
        if "height" in data:
            self.height = int(data['height'])
        if "width" in data:
            self.width = int(data['width'])
        if "model" in data:
            self.model_id = data['model']
            self.load()
        count = 10
        if "count" in data:
            count = int(data['count'])
        self.loop(count)
    def executeJsonFile(self, file, delete=True):
        data = json.load(open(file))
        self.execute(data)
        if delete:
            os.remove(file)
    def executeMany(self, data, count = 50):
        for key in data:
            self.prompt = data[key]
            self.prefix = key
            self.loop(count)
    def executeJobs(self, data):
        self.info("Start: "+time.strftime("%Y-%m-%d, %H:%M:%S", time.localtime()))
        jobs = data['jobs']
        i = 0
        for job in jobs:
            self.info("Job " + str(i) + "/" + str(len(jobs)) )
            self.execute(job)
            i=i+1
        result_url = data['result_url']
        files = {'upload_file': open('data.db', 'rb')}
        params = {'name': data['worker_name'], 'g': data['group_id']}
        res = requests.post(result_url, params=params, files=files)
        print(res.text)
        self.info("End: "+time.strftime("%Y-%m-%d, %H:%M:%S", time.localtime()))
        return i
    def executeFromUrl(self, url):
        res = requests.get(url)
        data = json.loads(res.text)
        return self.executeJobs(data)
    def info(self, message):
        print("[INFO] " + message)
            
            
        
class ImageGenProcess(ticker.FileExtObserver):
    ext = ".sdjob"
    def __init__(self, generator):
        self.generator = generator
    def processFile(self, filename):
        self.generator.executeJsonFile(filename)
