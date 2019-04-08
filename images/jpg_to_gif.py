import os,sys
import datetime
import imageio
from pprint import pprint
import time
import datetime
e=sys.exit

 
def create_gif(img_fd_name, duration):

	# filename: "abc.ext"
	# dirname: "dir0"
	# path: "dir0/dir1/abc.ext"
	# dir: "dir0/dir1"

	print("creating...")
	print("duration: {}".format(duration))

	img_dir = os.path.join(os.getcwd(), img_fd_name)
	print(img_dir)

	img_fps = sorted([
		os.path.join(img_dir, fn) for fn in os.listdir(img_dir)
		if fn.endswith(".png") and os.path.isfile(os.path.join(img_dir, fn))
	])
 	
	images = []
	for img_fp in img_fps:
		images.append(imageio.imread(img_fp))
	img_fn = 'Gif-%s.gif' % datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S')
	img_fp = os.path.join(img_fd_name, img_fn)
	imageio.mimsave(img_fp, images, duration=duration)
	print("complete")
 
 
if __name__ == "__main__":

	img_fd_name = str(sys.argv[1])
	
	duration = 0.1	
	if len(sys.argv) > 2:
		duration = float(sys.argv[2])

	create_gif(img_fd_name, duration)