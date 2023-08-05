#
#
# def install_package(package, version="upgrade"):
#     from sys import executable
#     from subprocess import check_call
#     result = False
#     if version.lower() == "upgrade":
#         result = check_call([executable, "-m", "pip", "install", package, "--upgrade", "--user"])
#     else:
#         from pkg_resources import get_distribution
#         current_package_version = None
#         try:
#             current_package_version = get_distribution(package)
#         except Exception:
#             pass
#         if current_package_version is None or current_package_version != version:
#             installation_sign = "==" if ">=" not in version else ""
#             result = check_call([executable, "-m", "pip", "install", package + installation_sign + version, "--user"])
#     print(result)
#     # return result
