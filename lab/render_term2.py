import sys, re
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FS = 16
font = ImageFont.truetype(FONT_PATH, FS)
bold = ImageFont.truetype(BOLD_PATH, FS)
BG=(13,15,20); FG=(222,226,230); CYAN=(88,196,221); GREEN=(134,196,100)
YELLOW=(224,196,108); GREY=(120,128,140)
ansi_re = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')

def color_for(line):
    if 'Status: 200' in line or '-> 200' in line:
        return GREEN
    if 'Status: 301' in line or 'Status: 403' in line:
        return YELLOW
    if '-> 404' in line or 'closed' in line:
        return GREY
    if line.strip().startswith(';;'):
        return GREY
    if 'open' in line and 'PORT' not in line:
        return GREEN
    return FG

def process_raw(raw):
    # split on \r and \n, strip ansi, drop empty/pure-progress lines
    raw = raw.replace('\r', '\n')
    out = []
    for line in raw.split('\n'):
        line = ansi_re.sub('', line)
        if not line.strip():
            continue
        if re.match(r'^:: Progress.*Errors: 0 ::\s*$', line.strip()):
            continue
        out.append(line)
    return out

def render(lines, out_path, prompt_lines, width=1000):
    pad=18; line_h=FS+7
    all_lines=[('prompt',p) for p in prompt_lines]+[('out',l) for l in lines]
    height = pad*2 + line_h*len(all_lines)+10
    img = Image.new('RGB',(width,height),BG); d=ImageDraw.Draw(img)
    y=pad
    for kind,text in all_lines:
        if kind=='prompt':
            if text.startswith('└─$'):
                d.text((pad,y),'└─$ ',font=bold,fill=CYAN)
                d.text((pad+d.textlength('└─$ ',font=bold),y),text[4:],font=bold,fill=FG)
            else:
                d.text((pad,y),text,font=bold,fill=CYAN)
        else:
            d.text((pad,y),text,font=font,fill=color_for(text))
        y+=line_h
    img.save(out_path)

if __name__=='__main__':
    cmd=sys.argv[1]; outfile=sys.argv[2]; txtfile=sys.argv[3]
    prompt=["┌──(godwin㉿kali)-[~]", f"└─$ {cmd}"]
    with open(txtfile) as f: raw=f.read()
    lines = process_raw(raw)
    render(lines, outfile, prompt)
