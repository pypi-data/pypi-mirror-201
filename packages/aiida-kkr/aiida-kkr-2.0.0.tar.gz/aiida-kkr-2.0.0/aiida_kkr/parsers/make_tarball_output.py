import tarfile
import os

n = load_node(134870)
r = n.outputs.retrieved

_FILENAME_TAR = 'output_all.tar.gz'

# check if output has been packed to tarfile already
# only if tarfile is not there we create the output tar file
if _FILENAME_TAR not in r.list_object_names():
    # first create dummy file which is used to extract the full path that is given to tarfile.open
    with r.open(_FILENAME_TAR, 'w') as f:
        filepath_tar = f.name
   
    # now create tarfile and loop over content of retrieved directory
    with tarfile.open(filepath_tar, 'w:gz') as tf:
        print tf.name
        to_delete = []
        for f in r.list_object_names():
            with r.open(f) as ftest:
                filesize = os.stat(ftest.name).st_size
                ffull = ftest.name
            if f != 'output_all.tar.gz' and filesize>0:
                tf.add(ffull, arcname=os.path.basename(ffull))
                to_delete.append(f)
        # finally delete files that have been added to tarfile
        for f in to_delete:
            r.delete_object(f) # force=True)

"""
 tar_filenames = []
 if _FILENAME_TAR in r.list_object_names():
     with r.open(_FILENAME_TAR) as tf:
         tfpath = tf.name
     with tarfile.open(tfpath) as tf:
         print tf.list()
         tar_filenames = [ifile.name for ifile in tf.getmembers()]
         tf.extractall()
"""
