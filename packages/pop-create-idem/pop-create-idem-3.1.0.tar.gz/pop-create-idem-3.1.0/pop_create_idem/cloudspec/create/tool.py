import pathlib

from cloudspec import CloudSpec


def run(hub, ctx, root_directory: pathlib.Path):
    if isinstance(root_directory, str):
        root_directory = pathlib.Path(root_directory)
    cloud_spec = CloudSpec(**ctx.cloud_spec)
    tool_dir = root_directory / ctx.clean_name / "tool" / ctx.service_name

    for ref, plugin in cloud_spec.plugins.items():
        mod_file = hub.cloudspec.parse.plugin.touch(tool_dir, ref)
        ref = hub.cloudspec.parse.plugin.ref(ctx, ref)
        module_ref = hub.cloudspec.parse.plugin.mod_ref(ctx, ref, plugin)

        # Set up the base template
        if not plugin.functions:
            to_write = hub.cloudspec.parse.plugin.header(plugin)
        else:
            to_write = hub.cloudspec.parse.plugin.header(plugin)
            for func_name, func_data in plugin.functions.items():
                if func_name in [
                    "get",
                    "list",
                    "create",
                    "update",
                    "delete",
                    "present",
                    "absent",
                    "describe",
                ]:
                    # These functions are not for tool module
                    continue

                template = hub.tool.jinja.template(
                    f"{hub.cloudspec.template.tool.FUNCTION}\n    {cloud_spec.request_format[func_name]}\n\n"
                )

                to_write += template.render(
                    function=dict(
                        name=func_name,
                        ref=ref,
                        module_ref=f"tool.{module_ref}",
                        **func_data,
                        header_params=hub.cloudspec.parse.param.headers(
                            func_data.params
                        ),
                    ),
                    parameter=dict(
                        mapping=hub.cloudspec.parse.param.mappings(func_data.params)
                    ),
                )

        mod_file.write_text(to_write)
