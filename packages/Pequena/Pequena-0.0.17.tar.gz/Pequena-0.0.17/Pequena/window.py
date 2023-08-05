import webview
import re
import os
from distutils.dir_util import copy_tree


build_dir = "./build"
client_dir = ""
client_html = ""
build_html = ""
win_name = ""


def getWindowInfo():
    return {"x": webview.windows[0].x, "y": webview.windows[0].y, "width": webview.windows[0].width, "height": webview.windows[0].height}


def minimizeWindow():
    return webview.windows[0].minimize()


def unminimizeWindow():
    return webview.windows[0].restore()


def hideWindow():
    return webview.windows[0].hide()


def unhideWindow():
    return webview.windows[0].show()


def toggleFullscreen():
    return webview.windows[0].toggle_fullscreen()


def moveWindow(_x, _y):
    return webview.windows[0].move(_x, _y)


def resizeWindow(_width, _height):
    return webview.windows[0].resize(_width, _height)


def setWindowName(_name):
    return webview.windows[0].set_title(_name)


def readFile(path):
    with open(path, 'r') as file:
        return file.read()


def writeFile(path, content):
    with open(path, 'w') as file:
        file.write(content)


def mkdir(path):
    os.mkdir(path)


def readdir(path):
    return os.listdir(path)


def pathExists(path):
    return os.path.exists(path)


def isfile(path):
    return os.path.isfile(path)


def isdir(path):
    return os.path.isdir(path)


exposed_fcs = [getWindowInfo, minimizeWindow, unminimizeWindow, hideWindow, unhideWindow, toggleFullscreen,
               moveWindow, resizeWindow, setWindowName, readFile, writeFile, mkdir, readdir, pathExists, isfile, isdir]


def expose_function(fc):
    exposed_fcs.append(fc)
    print("exposed: " + str(exposed_fcs))


def check_for_modules(js_path):
    script_dir = os.path.dirname(js_path)
    script_str = ""
    with open(js_path, 'r') as f:
        script_content = f.readlines()

    for line in script_content:
        if ("import" in line):
            import_regex = re.compile(r'from \".+\"|from \'.+\'')
            module_path = script_dir + "/" + import_regex.findall(line)[0].replace("from ", "").replace(
                "\"", "").replace("\'", "")
            script_str += check_for_modules(module_path)
        else:
            if (not "export \{" in line):
                script_str += line.replace("export ", "")
    return script_str + "\n"


def handle_build_copy():
    if not os.path.exists(client_dir):
        return
    try:
        copy_tree(client_dir, build_dir)
    except:
        print("from Copy tree")
        return
    script_str = "<script>window.addEventListener('pywebviewready', function () {\nconst PEQUENA = pywebview.api\n"
    new_html = ""
    with open(build_html, 'r') as f:
        html_content = f.readlines()

    for line in html_content:
        if ("<script" in line):
            if ("src=" in line):
                file_regex = re.compile(r'(?:href|src)="([^"]+)"')
                js_path = os.path.dirname(build_html) + \
                    "/" + file_regex.findall(line)[0]
                if ("type=\"module\"" in line):
                    script_str += check_for_modules(js_path)
                else:
                    print("JS_PATH: ", js_path)
                    with open(js_path, 'r', errors='ignore') as f:
                        script_str += f.read() + "\n"
        else:
            new_html += line

    new_html = new_html.replace("</body>", script_str + "})</script>\n</body>")
    with open(build_html, "w") as op:
        op.write(new_html)


def init(client_src, window_name="Hello World!"):
    global client_dir
    global client_html
    global build_html
    global win_name

    win_name = window_name
    client_dir = os.path.dirname(client_src)
    client_html = os.path.basename(client_src)
    build_html = build_dir + "/" + client_html
    handle_build_copy()


def create_window(width=800, height=600,
                  x=None, y=None, resizable=True, fullscreen=False, min_size=(200, 100),
                  hidden=False, frameless=False, easy_drag=True,
                  minimized=False, on_top=False, confirm_close=False, background_color='#FFFFFF',
                  transparent=False, text_select=False, zoomable=False, draggable=False, port=0, debug=True):
    window = webview.create_window(title=win_name, url=build_html, width=width, height=height,
                                   x=x, y=y, resizable=resizable, fullscreen=fullscreen, min_size=min_size,
                                   hidden=hidden, frameless=frameless, easy_drag=easy_drag,
                                   minimized=minimized, on_top=on_top, confirm_close=confirm_close, background_color=background_color,
                                   transparent=transparent, text_select=text_select, zoomable=zoomable, draggable=draggable)
    for fc in exposed_fcs:
        window.expose(fc)
    if (port != 0):
        webview.start(gui='edgehtml', debug=debug, http_port=port)
    else:
        webview.start(gui='edgehtml', debug=debug)
