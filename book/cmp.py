import sys, glob
from PIL import Image
n = sys.argv[1]
ims = [Image.open(f).convert('RGB') for f in sorted(glob.glob(f'../figures-atlas/ms/{n}_*.jpg'))] + [Image.open(f'out/fig/{n}.png').convert('RGB')]
h = int(sys.argv[2]) if len(sys.argv) > 2 else 560
ims = [i.resize((max(1, int(i.width * h / i.height)), h)) for i in ims]
c = Image.new('RGB', (sum(i.width for i in ims) + 20 * len(ims), h), 'white'); x = 0
for i in ims: c.paste(i, (x, 0)); x += i.width + 20
c.save(f'/tmp/claude-0/-home-user-biruni-istiaab/2bd96094-8275-54f9-a79a-136e87f6567c/scratchpad/cmp_{n}.jpg', quality=85)
