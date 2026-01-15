import sys
import os
import bpy
import importlib

bl_info = {
    "name": "Joy2view3Dctrl_v3_test(qtn)",
    "author": "HEN3TO",
    "version": (0, 6),
    "blender": (4, 1, 0),
    "location": "3Dビューポート > Sidebar >  Joy2view",
    "description": "3D VIEW CONTROL by NDOF Joysticks",
    "warning": "",
    #"support": "TESTING",
    "doc_url": "",
    "tracker_url": "",
    "category": "Object"
}



# アドオンのルートディレクトリを取得
addon_root = os.path.dirname(__file__)
# libsフォルダへのパスを作成
libs_path = os.path.join(addon_root, "libs")

# sys.path に追加（二重登録を防ぐチェック付き）
if libs_path not in sys.path:
    sys.path.append(libs_path)

# これで準備完了。通常通り import できる。
try:
    import pygame
    print("pygame 2.5.1の読み込みに成功しました")
except ImportError as e:
    print(f"pygame 2.5.1が見つかりません: {e}")



from . import v3_modal_orbit_qtn as main
classes = [
    main.J2V3D_OT_Joy2view3Dctrl,
    main.J2V3D_OT_Inithprops,
    main.J2V3D_OT_Refreshprops,
    main.J2V3D_PT_Joy2view3Dctrl,
    main.J2V3D_PT_settings
]

def register():
    # 登録処理
    for c in classes:
        bpy.utils.register_class(c)
    
    main.init_props()
    print("J2V3D: アドオン『Joy2view3Dctrl』が有効化されました。")
    pass

def unregister():
    # 削除時、必要なら sys.path から libs_path を取り除く
    if libs_path in sys.path:
        sys.path.remove(libs_path)
    for c in classes:
        bpy.utils.unregister_class(c)
    main.clear_props()
    print("J2V3D: アドオン『Joy2view3Dctrl』が無効化されました。")