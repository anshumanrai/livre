import sys, string, os, datetime, time, glob, subprocess, re, fnmatch
#UNIX version (slashes = / )
def parallelCommands(cmds, numThreads):
    if not cmds: return # empty list

    def done(p):
        return p.poll() is not None
    def success(p):
        return p.returncode == 0;
    def fail():
        sys.exit(1);

    max_task = numThreads;
    processes = [] ;
    while True:
        while cmds and len(processes) < max_task:
            task = cmds.pop();
            print (task);
            processes.append(subprocess.Popen(task, shell=True));

        for p in processes:
            if done(p):
                if success(p):
                    processes.remove(p);
                else:
                    fail();

        if not processes and not cmds:
            break
        else:
            time.sleep(0.05);

currFolder = os.path.dirname(os.path.realpath(__file__));

rootFolder = "%s/videos/" % currFolder; #Videos Root Folder. Change this path if necessary. Attention windows/unix slash direction

overwriteExtractKeyframes = True;

keyframeRate = 1;
keyframeHeight = 480;
numThreads = 3;
extractKeyframesScript = "python %s/extractParseUNIX.py" % currFolder;
print (extractKeyframesScript);

extractKeyframesCommands = [];

# Write a list of all videos on the rootFolder to a file. Recursive.

outputVideosList = "videoFiles.txt" 
types = ('*.mp4', '*.webm', '*.ogv', '*.avi' ) # the tuple of file types supported
videoFiles = []
for fileType in types:
	for root, dirs, files in os.walk(rootFolder):
		for filename in fnmatch.filter(files, fileType):
			videoFiles.append(os.path.join(root, filename))
			#print (os.path.join(root, filename))
#videoFiles.sort();  

fid = open(outputVideosList, 'w');
for videoFile in videoFiles:
	fid.write(videoFile + "\n");
fid.close();

# Generate extract and parse keyframes commands
print("Overwrite Extracted Keyframes is set to: " + str(overwriteExtractKeyframes) + ".\n You can change this option inside the python file" );
for videoFile in videoFiles:
	name, ext = os.path.splitext(videoFile);
	outputFolder = name + "_keyframes";
	if (not os.path.exists(outputFolder)) or overwriteExtractKeyframes:
		
		extractCmd = "%s %s %s %d scale=-1:%d" % (extractKeyframesScript, videoFile, outputFolder, keyframeRate, keyframeHeight);
        chmodCmd = "chmod -R a+rw %s" % outputFolder; #Change permissions of generated images (UNIX)
		extractKeyframesCommands.append(extractCmd + "; " + chmodCmd); # (UNIX)
		
		continue;

# Extract keyframes, convert keyframes
parallelCommands(extractKeyframesCommands, numThreads);
	
#TODO: Promt user if he wants to proceed with parsing

#in = input("Enter (y)es or (n)o: ") 
#if in == "yes" or in == "y": 
# 	print("Do whatever you need to do here after yes") 
#elif in == "no" or in == "n": 
# 	print("Do whatever you need to do here after no") 
#parallelCommands(extractFeaturesCommands, 1); # feature extraction already contains parallelization
	

