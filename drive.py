from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from striprtf.striprtf import rtf_to_text
from game import Game

'''
CITATIONS 

I used these websites to learn/piece together code for this
https://stackoverflow.com/questions/60897366/how-to-read-rtf-file-and-convert-into-python3-strings-and-can-be-stored-in-pyth
https://stackoverflow.com/questions/55708541/pydrive-how-to-read-a-file-by-id-title
https://pypi.org/project/striprtf/
https://docs.python.org/3/library/os.path.html#module-os.path
https://pypi.org/project/PyDrive/
https://www.geeksforgeeks.org/run-one-python-script-from-another-in-python/
https://pythonhosted.org/PyDrive/filemanagement.html
https://stackoverflow.com/questions/67623860/how-to-access-shared-google-drive-files-through-python

It's not all directly copy pasted but I referred to it when I had to figure out how to do this so some parts are similar

Used ChatGPT to figure out lines 47-54, was not aware of the documentation to download folders so it helped me with that part, the code was bad so I ended up having to make changes but it provided the base structure

'''

def getUserContent(imagesFolderLink, topic, answer, infoFileLink, imageType):
    googleAuth = GoogleAuth()
    googleAuth.LocalWebserverAuth()
    googleDrive = GoogleDrive(googleAuth)

    folderId = imagesFolderLink.split('/')
    folderId = folderId[-1]
    imagePath = './images/'
    imagePath = f'./images/{topic}'
    fileId = infoFileLink.split('/')[-2]
    infoFileName = googleDrive.CreateFile({'id': fileId})
    infoFileName.GetContentFile(infoFileName['title'])
    title = infoFileName['title']
    # read the context from the text file
    with open (f'{title}') as infile:
        content = infile.read()
        text = rtf_to_text(content)
    topicsList = text.splitlines()[1:51]
    answersList = text.splitlines()[53:105]

    if not os.path.exists(imagePath):
        os.makedirs(imagePath)
    imageList = googleDrive.ListFile({'q': f"'{folderId}' in parents"}).GetList()
    # download the images
    for i in range(len(imageList)):
        image = imageList[i]
        imageName = topicsList[i]
        image.GetContentFile(os.path.join(imagePath, f'{imageName}.{imageType}'))
    
    newGame = Game(topic, getImagesList(topic, topicsList, imageType), topicsList, answersList, topic, answer, 'images/stateCapitalScreen.png')
    return newGame

def getImagesList(topic, topicsList, imageType):
    imagesList = []
    for subtopic in topicsList:
        imagesList.append(f'images/{topic}/{subtopic.lower()}.{imageType}')
    imagesList.append(f'images/states/add.png')
    imagesList.append(f'images/states/remove.png')
    return imagesList