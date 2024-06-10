# ------------------------------------------------------------------
# Python 3+ only!!!
# ------------------------------------------------------------------
import os
import hashlib
import locale

locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'


# ------------------------------------------------------------------
# Recull informació dels fitxers en una llista de directoris
# ------------------------------------------------------------------
def GetFilesInFolderInfo(folderList):
  filesInfo = [] 
  for folder in folderList:
    for path, subdirs, files in os.walk(folder): # També els subdirectoris
      for name in files:
        filename = os.path.join(path, name)
        filesize = os.stat(filename).st_size
        filesInfo.append( (filename, filesize) )
  
  return filesInfo
# ------------------------------------------------------------------


# ------------------------------------------------------------------
# De la llista de fitxers selecciona els que medeixen el mateix.
# Opcionalment llegeix i compara el seu contingut (calculant el seu hash MD5).
# ------------------------------------------------------------------
def BuiltDuplicatesDict(filesInfo, readContent=False):
  
  # Pas 1 de 2 (fitxers que medeixen el mateix)
  fdict = {}
  for e in filesInfo:
    filename = e[0]
    size = str(e[1]).zfill(13)

    if size not in fdict:
      fdict[size] = [] 
    fdict[size].append(filename)

  # Esborra els fitxers únics  
  for size in list(fdict.keys()):
    if len(fdict[size]) == 1: 
      del fdict[size]

  if not readContent: return fdict

  # Pas 2 de 2 (calcular MD5 dels fitxers que medeixen el mateix)
  count = 0
  for size in fdict:
    for filename in fdict[size]:
      count += 1
  print("Checking " + "{:n}".format(count) + " MD5 signatures...")

  count = 0
  fdict2 = {}
  for size in fdict:
    #print(size, fdict[size])
    for filename in fdict[size]:
      md5 = hashlib.md5(open(filename,'rb').read()).hexdigest()
      key = size +"."+ md5

      if key not in fdict2:
        fdict2[key] = [] 
      fdict2[key].append(filename)
      count += 1
      if count % 100 == 0: print("{:n}".format(count) + " MD5 signatures checked.")

  # Esborra els fitxers únics  
  for key in list(fdict2.keys()):
    if len(fdict2[key]) == 1: 
      del fdict2[key]

  return fdict2
# ------------------------------------------------------------------

        

folders = ["C:\\MY_DATA"] # Llista de directoris on cercar duplicats
files = GetFilesInFolderInfo(folders)
dups = BuiltDuplicatesDict(files, readContent=True) # readContent es molt lent!!!
print("Duplicate files in %s (sorted by size):\n" % folders)
for k in sorted(dups.keys(), reverse=True):
  print( "{:n}".format(int(k[:13]))+ " bytes:" )
  for e in dups[k]:
    print("  "+e)
  print()
