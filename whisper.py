import DaVinciResolveScript as dvr_script
resolve = dvr_script.scriptapp("Resolve")
import sys
import os
import time

def AddTimelineToRender( project, timeline, presetName, targetDirectory, renderFormat, renderCodec, timelinename ):
    project.SetCurrentTimeline(timeline)
    project.LoadRenderPreset(presetName)

    if not project.SetCurrentRenderFormatAndCodec(renderFormat, renderCodec):
        return False

    project.SetRenderSettings({"SelectAllFrames" : 1, "TargetDir" : targetDirectory, "ExportVideo": False, "ExportAudio" : True, "CustomName": timelinenamewhisper})
    return project.AddRenderJob()

def RenderAllTimelines( resolve, timeline, presetName, targetDirectory, renderFormat, renderCodec ):
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    if not project:
        return False

    resolve.OpenPage("Deliver")
    
    if not AddTimelineToRender(project, timeline, presetName, targetDirectory, renderFormat, renderCodec, timelinename):
        return False
    return project.StartRendering()

def IsRenderingInProgress( resolve ):
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    if not project:
        return False

    return project.IsRenderingInProgress()

def WaitForRenderingCompletion( resolve ):
    while IsRenderingInProgress(resolve):
        time.sleep(1)
    return

def DeleteAllRenderJobs( resolve ):
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    project.DeleteAllRenderJobs()
    return

renderPresetName = "H.264 Master"
renderPath = os.path.expanduser('~')
renderFormat = "mp4"
renderCodec = "H264"

# Get currently open project

projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
project.DeleteAllRenderJobs()
timeline = project.GetCurrentTimeline()
timelinename = timeline.GetName()
timelinename = timelinename.replace(" ", "")
timelinenamewhisper = timelinename + 'subwhisper'

if not RenderAllTimelines(resolve, timeline, renderPresetName, renderPath, renderFormat, renderCodec):
    print("Unable to set all timelines for rendering")
    sys.exit()

WaitForRenderingCompletion(resolve)

DeleteAllRenderJobs(resolve)

system = os.name

print("Rendering is completed.")
if system != 'posix':
    s = f"whisper {renderPath}\{timelinenamewhisper}.mp4 --language es --model medium --output_dir {renderPath}"
    video = f"{renderPath}\{timelinenamewhisper}.mp4"
    subtitulo = f"{renderPath}\{timelinenamewhisper}.mp4.srt"
else:
    s = f"whisper {renderPath}/{timelinenamewhisper}.mp4 --language es --model medium --output_dir {renderPath}"    
    video = f"{renderPath}/{timelinenamewhisper}.mp4"
    subtitulo = f"{renderPath}/{timelinenamewhisper}.mp4.srt"


os.system(s)

resolve.OpenPage("Edit")
mediapool = project.GetMediaPool()

mediapool.ImportMedia(subtitulo)
os.remove(video)
