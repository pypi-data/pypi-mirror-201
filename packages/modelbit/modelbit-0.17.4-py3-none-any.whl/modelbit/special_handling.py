from typing import Any

from .helpers import NamespaceCollection


def collectedSpecialObj(obj: Any, name: str, collection: NamespaceCollection) -> bool:
  if _inTypeStr("_FastText", obj):
    _collectFastText(obj, name, collection)
    return True
  return False


def savedSpecialObj(obj: Any, filepath: str):
  if _inTypeStr("_FastText", obj):
    obj.save_model(filepath)
    return True
  else:
    return False


def collectPipelineModules(obj: Any, collection: NamespaceCollection):
  if not _inTypeStr("sklearn.pipeline", obj):
    return
  try:
    for step in obj.steps:
      pipelineObj = step[1]
      if not hasattr(pipelineObj, "__class__") or not hasattr(pipelineObj, "__module__"):
        continue
      collection.froms[pipelineObj.__class__.__name__] = pipelineObj.__module__
      collection.allModules.append(pipelineObj.__module__)
  except:
    pass


def _inTypeStr(name: str, obj: Any) -> bool:
  return name in f"{type(obj)}"


def _collectFastText(obj: Any, name: str, collection: NamespaceCollection):
  import tempfile, os
  tmpFilePath = os.path.join(tempfile.gettempdir(), "tmp.pkl")
  assert savedSpecialObj(obj, tmpFilePath)
  with open(tmpFilePath, "rb") as f:
    collection.extraDataFiles[name] = (obj, f.read())
  collection.customInitCode.append(f"{name} = fasttext.load_model('data/{name}.pkl')")
  collection.imports["fasttext"] = "fasttext"
