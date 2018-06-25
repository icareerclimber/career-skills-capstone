# ssh-keygen -t rsa -b 4096 -C wheatley.keri@gmail.com && cat ~/.ssh/id_rsa.pub
# $ sudo apt-get install git && git clone git@github.com:datasci-w266/2018-spring-assignment-keriwheatley.git w266 && ./w266/assignment/a0/cloud/setup.sh && source ~/.bashrc  && pip install boto3 && pip install bs4 && git clone git@github.com:kbelsvik/career-skills-capstone.git skills && screen -R main
# gsutil cp gs://w210_capstone_models/traindocs .
# conda config --add channels conda-forge
# conda install gensim
# sudo rm -f /etc/boto.cfg


import datetime
import pickle
from gensim.models import Doc2Vec

print("Loading pickled documents", datetime.datetime.now())
traindocs = pickle.load(open('traindocs', 'rb'))

parameters = {
                "dm":1,
                "vector_size":300, # changed from 200
                "alpha":0.025,
                "min_alpha":0.001,
                "min_count":5, # changed from 5
                "sample":0,
                "workers":4,
                "epochs":1,
                "negative":5, # default
                "total_examples":1200000
}

for key in parameters:
    print(key, parameters[key])


print("Starting instantiate model", datetime.datetime.now())
model = Doc2Vec(traindocs, 
                              dm=parameters["dm"],
                              vector_size=parameters["vector_size"],
                              alpha=parameters["alpha"],
                              min_alpha=parameters["min_alpha"],
                              min_count=parameters["min_count"],
                              sample=parameters["sample"],
                              workers=parameters["workers"],
                              negative=parameters["negative"]
                             )
print("End instantiate model", datetime.datetime.now())


print("Starting train", datetime.datetime.now())
model.train(traindocs, total_examples=parameters["total_examples"], epochs=parameters["epochs"])
print("End train", datetime.datetime.now())


print("Starting save model", datetime.datetime.now())

save_time = str(datetime.datetime.now())
model.save("models/" + save_time + '_model.doc2vec')

write_param = open("models/" + save_time + '_parameters.txt','w')
for key in parameters:
    write_param.write(key + "=" + str(parameters[key]) + '\n')
write_param.close()

print("End save model", datetime.datetime.now())
