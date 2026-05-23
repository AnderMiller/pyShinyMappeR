These are notes for a mini-refactor of how the current structure will be changed.

Currently:
pyShinyMapper has classes for types of results for each aspect of mapper:
data, lens, coverer, clusterer. All of the logic for combining these is done 
inside of server.py which I suspect will be confusing to people looking to 
extend it.

Change:
1. VisualizationModules should be Protocols
2. ui-builder should contain helpers for updating the ui
3. Plugins take in context/state module and declare dependencies


Goals:
1. All logic needs to be able to be isolated inside of individual modules.
that way contributors only need to work inside of one file.
2. move update slider into ui_builder and out of server
3. add: Context, UIController, Registery, VisualizationProtocol

Module[Context + UIController] -> Registry[event] -> callback func

Then the server is just high-level reactives for modules and mapper:

```python
@reactive.effect
def _on_mapper_change():
    result = current_mapper_result()
    # update modules that registered for 'cover_count'
    for callback in REGISTRY.get("cover_count", []):
        callback(plugin_context, current_vid)
```
