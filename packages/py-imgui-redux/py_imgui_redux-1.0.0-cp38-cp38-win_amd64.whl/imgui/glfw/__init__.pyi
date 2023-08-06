"""GLFW Backend Wrapper"""
from __future__ import annotations
import imgui.glfw
import typing
import imgui

__all__ = [
    "Init",
    "InitContextForGLFW",
    "NewFrame",
    "Render",
    "ShouldClose",
    "Shutdown"
]


def Init(window_width: int, window_height: int, title: str, swap_interval: int = 1) -> capsule:
    pass
def InitContextForGLFW(window: capsule) -> None:
    pass
def NewFrame() -> None:
    pass
def Render(window: capsule, clear_color: imgui.Vec4) -> None:
    pass
def ShouldClose(window: capsule) -> bool:
    pass
def Shutdown(window: capsule) -> None:
    pass
