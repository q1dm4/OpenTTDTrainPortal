#!/usr/bin/env python3
"""Generate original, precisely aligned code-native gateway sprite assets."""
from pathlib import Path
from math import sin, cos, pi
from PIL import Image, ImageDraw
from nml.palette import raw_palette_data
ROOT = Path(__file__).resolve().parents[1]
W, H, FRAMES = 64, 80, 8
sheet = Image.new('RGB', (W * 4, H * FRAMES), (0, 0, 255))
# Pixel coordinate basis for OpenTTD's two diagonal railway orientations.
def point(axis, across, up):
    sx, sy = ((2, 1) if axis == 0 else (-2, 1))
    return (round(32 + across * sx), round(65 + across * sy - up))
for frame in range(FRAMES):
    brightness = round(170 + 65 * (1 + sin(2*pi*frame/FRAMES))/2)
    for axis in range(2):
        # Separate near/far halves let vehicles sort between the ring supports.
        for half in range(2):
            im = Image.new('RGB', (W, H), (0, 0, 255)); d = ImageDraw.Draw(im)
            for side in [-1, 1]:
                if (side > 0) != (half == 1): continue
                p = point(axis, side * 10, 0)
                d.polygon([(p[0]-6,p[1]-2),(p[0],p[1]-5),(p[0]+6,p[1]-2),(p[0],p[1]+2)], fill=(70,80,95), outline=(120,135,150))
            pts = []
            for step in range(65):
                angle = pi * step / 64
                across, up = 11*cos(angle), 4+42*sin(angle)
                if (across >= 0) != (half == 1):
                    if len(pts)>1: d.line(pts, fill=(48,65,80), width=7)
                    pts=[]; continue
                pts.append(point(axis, across, up))
            if len(pts)>1: d.line(pts, fill=(48,65,80), width=7)
            # Cyan inner strip and light cells.
            pts=[]
            for step in range(65):
                angle=pi*step/64; across=11*cos(angle); up=4+42*sin(angle)
                if (across>=0)!=(half==1):
                    if len(pts)>1: d.line(pts, fill=(30,brightness,255), width=3)
                    pts=[]; continue
                pts.append(point(axis,across,up))
            if len(pts)>1: d.line(pts, fill=(30,brightness,255), width=3)
            for step in range(1,12):
                angle=pi*step/12; across=11*cos(angle)
                if (across>=0)!=(half==1): continue
                p=point(axis,across,4+42*sin(angle)); d.point(p,fill=(220,255,255))
            sheet.paste(im,(W*(axis*2+half),H*frame))
pal = Image.new('P',(1,1)); pal.putpalette(raw_palette_data[0])
indexed = sheet.quantize(palette=pal,dither=Image.Dither.NONE)
# Reserve palette index zero explicitly for transparency.
px=indexed.load()
for y in range(sheet.height):
    for x in range(sheet.width):
        if sheet.getpixel((x,y))==(0,0,255): px[x,y]=0
indexed.info['transparency'] = 0
indexed.save(ROOT/'newgrf/gateway.png', transparency=0)
# Preview is a development visualization, not a game screenshot.
preview=Image.new('RGB',(560,300),(20,29,39)); d=ImageDraw.Draw(preview)
d.text((20,15),'ENERGY GATEWAY - ORIGINAL SPRITES / BOTH RAIL AXES',fill=(224,238,247))
for axis in range(2):
    tile=Image.new('RGBA',(64,80)); td=ImageDraw.Draw(tile)
    td.polygon([(0,64),(32,48),(63,64),(32,79)],fill=(55,73,68))
    for offset in [-3,3]:
        if axis==0: td.line([(offset,64),(32+offset,48)],fill=(168,178,182),width=2); td.line([(32+offset,79),(63+offset,64)],fill=(168,178,182),width=2)
        else: td.line([(0+offset,64),(32+offset,79)],fill=(168,178,182),width=2); td.line([(32+offset,48),(63+offset,64)],fill=(168,178,182),width=2)
    for half in range(2):
        spr=indexed.crop((W*(axis*2+half),0,W*(axis*2+half+1),H)).convert('RGBA')
        tile.alpha_composite(spr)
    large=tile.resize((256,256),Image.Resampling.NEAREST)
    preview.paste(large,(20+axis*280,40),large)
preview.save(ROOT/'docs/gateway-preview.png')
# Build NML from the fixed frame table; the source is also shipped.
base=(ROOT/'newgrf/gateway.nml').read_text().split('// GENERATED SPRITES')[0]
out=[base,'// GENERATED SPRITES\n']
for f in range(FRAMES):
    out.append(f'spriteset (gateway_frame_{f}, "gateway.png") {{\n')
    for col in range(4): out.append(f'    [{col*W}, {f*H}, {W}, {H}, -31, -64]\n')
    out.append('}\n')
for axis,name in enumerate(['X','Y']):
    out.append(f'''spritelayout gateway_{name} {{
    ground {{ sprite: {1012 if axis == 0 else 1011}; }}
    building {{ sprite: DEFAULT({axis*2}); xoffset: 0; yoffset: 0; zoffset: 0; xextent: 16; yextent: 4; zextent: 48; }}
    building {{ sprite: DEFAULT({axis*2+1}); xoffset: 0; yoffset: 12; zoffset: 0; xextent: 16; yextent: 4; zextent: 48; }}
}}
''')
for f in range(FRAMES): out.append(f'spritegroup gateway_group_{f} {{ little: gateway_frame_{f}; lots: gateway_frame_{f}; }}\n')
out.append('switch(FEAT_STATIONS, SELF, gateway_animation, animation_frame) {\n')
for f in range(FRAMES): out.append(f'    {f}: gateway_group_{f};\n')
out.append('    gateway_group_0;\n}\n')
out.append('''item(FEAT_STATIONS, energy_gateway, 0) {
    property {
        class: "TGWY";
        classname: string(STR_CLASS);
        name: string(STR_GATEWAY);
        disabled_platforms: bitmask(2,3,4,5,6,7,8);
        disabled_length: bitmask(2,3,4,5,6,7,8);
        tile_flags: [0,0];
        animation_info: [ANIMATION_LOOPING,8];
        animation_speed: 3;
        animation_triggers: bitmask(ANIM_TRIGGER_STAT_BUILT);
    }
    graphics {
        sprite_layouts: [gateway_X,gateway_Y];
        select_tile_type: 0;
        anim_control: 0;
        purchase: gateway_frame_0;
        gateway_animation;
    }
}
''')
(ROOT/'newgrf/gateway.nml').write_text(''.join(out))
print('Generated 8 animation frames, 2 orientations, split ring sprites.')
