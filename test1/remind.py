import platform
from datetime import datetime, time


def platform_method(platform_name):
    """
    装饰器，用于标注平台特定的方法。

    Args:
        platform_name (str): 平台名称

    Returns:
        function: 装饰后的函数。
    """

    def decorator(func):
        _platform_name = platform_name.lower()
        if _platform_name == "mac":
            _platform_name = "darwin"

        func._platform_name = _platform_name
        return func

    return decorator


class PlatformMethodRegistry(type):
    def __new__(cls, name, bases, attrs):
        platform_methods = {}
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and hasattr(attr_value, "_platform_name"):
                platform_name = attr_value._platform_name
                if platform_name in platform_methods:
                    raise Exception(f"平台 '{platform_name}' 已经存在多个实现。")
                platform_methods[platform_name] = attr_value
        attrs["_platform_methods"] = platform_methods
        return super().__new__(cls, name, bases, attrs)


class PlatformDispatchMixin(metaclass=PlatformMethodRegistry):
    @classmethod
    def dispatch(cls, *args, **kwargs):
        current_os = platform.system().lower()
        platform_methods = cls._platform_methods.get(current_os)
        if not platform_methods:
            raise NotImplementedError(
                f"当前操作系统 '{platform.system()}' 未实现对应的逻辑。"
            )
        return platform_methods(cls, *args, **kwargs)


class ScreenStatusChecker(PlatformDispatchMixin):
    def is_screen_on(self):
        return self.dispatch()

    @platform_method("windows")
    def _windows_screen_status(self, *args, **kwargs):
        try:
            import win32gui
        except ImportError as e:
            raise ImportError(
                "需要安装 'pywin32' 模块，请使用命令 'pip install pywin32' 进行安装。"
            ) from e

        hwnd = win32gui.GetForegroundWindow()
        return hwnd != 0

    @platform_method("darwin")
    def _darwin_screen_status(self, *args, **kwargs):
        try:
            from Quartz import CGDisplayIsAsleep
        except ImportError as e:
            raise ImportError(
                "需要安装 'Quartz' 模块，请使用命令 'pip install pyobjc-framework-Quartz' 进行安装。"
            ) from e

        is_asleep = CGDisplayIsAsleep(0)
        return not is_asleep

    @platform_method("linux")
    def _linux_screen_status(self, *args, **kwargs):
        import subprocess

        try:
            output = subprocess.check_output(
                ["xset", "-q"], stderr=subprocess.STDOUT
            ).decode()
            for line in output.splitlines():
                if "Monitor is" in line:
                    status = line.strip().split("Monitor is")[-1].strip()
                    return status.lower() == "on"
            raise Exception("无法从 xset 输出中确定显示器状态。")
        except FileNotFoundError:
            raise Exception(
                "未找到 'xset' 命令。请确保已安装该命令（例如，使用 'sudo apt-get install x11-xserver-utils'）。"
            )
        except subprocess.CalledProcessError as e:
            raise Exception(f"执行 'xset' 命令时发生错误：{e}")
        except Exception as e:
            raise Exception(f"检测显示器状态时发生错误：{e}")


class MessageNotifier(PlatformDispatchMixin):
    def send_notification(self, title, message):
        return self.dispatch(title, message)

    @platform_method("windows")
    def _windows_notification(self, title, message):
        try:
            from win10toast import ToastNotifier
        except ImportError as e:
            raise ImportError(
                "需要安装 'win10toast' 模块，请使用命令 'pip install win10toast' 进行安装。"
            ) from e

        toaster = ToastNotifier()
        toaster.show_toast(title, message, icon_path=None, duration=5, threaded=True)

    @platform_method("darwin")
    def _darwin_notification(self, title, message):
        import subprocess

        try:
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(["osascript", "-e", script], check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"执行 'osascript' 命令时发生错误：{e}")
        except Exception as e:
            raise Exception(f"发送通知时发生错误：{e}")

    @platform_method("linux")
    def _linux_notification(self, title, message):
        import subprocess

        try:
            subprocess.run(["notify-send", title, message], check=True)
        except FileNotFoundError:
            raise Exception(
                "未找到 'notify-send' 命令。请确保已安装该命令（例如，使用 'sudo apt-get install libnotify-bin'）。"
            )
        except subprocess.CalledProcessError as e:
            raise Exception(f"执行 'notify-send' 命令时发生错误：{e}")
        except Exception as e:
            raise Exception(f"发送通知时发生错误：{e}")


try:
    check = ScreenStatusChecker()
    if check.is_screen_on():
        print("屏幕当前处于开启状态。")
        MessageNotifier().send_notification("提醒", "快跑")
    else:
        print("屏幕已关闭或处于锁定状态。")
except Exception as e:
    print(f"错误：{e}")

