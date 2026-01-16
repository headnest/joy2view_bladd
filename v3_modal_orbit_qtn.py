import datetime
import pygame
import bpy
from mathutils import Euler, Vector
from math import radians





# オペレータ
class J2V3D_OT_Joy2view3Dctrl(bpy.types.Operator):

    bl_idname = "view3d.joy2view_ctrl_3dview"
    bl_label = "3DviewControling"
    bl_description = "Dinputデバイスで3Dviewを操作します"
    __pg_joys_obj = None
    # タイマのハンドラ
    __timer = None
    # テキストオブジェクトの名前
    __text_object_name = None
    __0jyosan_blocker = 0.0000001

    settings = {"input":1,"pan_z":0,"pan_x":1,"t_x":3,"t_y":4,"zoom":5}

    @classmethod
    def is_running(cls):
        # モーダルモード中はTrueを返す
        return True if cls.__timer else False

    def __handle_add(self, context):
        if not self.is_running():
            # タイマを登録
            J2V3D_OT_Joy2view3Dctrl.__timer = \
                context.window_manager.event_timer_add(
                    0.01, window=context.window
                )
            # モーダルモードへの移行
            context.window_manager.modal_handler_add(self)

    def __handle_remove(self, context):
        if self.is_running():
            # タイマの登録を解除
            context.window_manager.event_timer_remove(
                J2V3D_OT_Joy2view3Dctrl.__timer)
            J2V3D_OT_Joy2view3Dctrl.__timer = None

    def modal(self, context, event):
        op_cls = J2V3D_OT_Joy2view3Dctrl

        # エリアを再描画
        if context.area:
            context.area.tag_redraw()

        # パネル最上部の [Stop input(now:active)] を押したときに、モーダルモードを終了
        if not self.is_running():
            return {'FINISHED'}

        if event.type == 'TIMER':
            pygame.event.clear()
            area = None
            #finding view area
            """多分いらない invoke()内でこの辺の処理完結済み
            try:
                for i in bpy.data.window_managers[0].windows[0].screen.areas:
                    if i.type == "VIEW_3D":
                        area = i
            except:
                area = None
            print(area)
            if area is None:
                print("view area not find")
                return {'PASS_THROUGH'}
            """

            _jb = op_cls.__0jyosan_blocker
            """

            ax0x_ang = (op_cls.__pg_joys_obj.get_axis(0)+_jb)/20.0
            ax0y_ang = (op_cls.__pg_joys_obj.get_axis(1)+_jb)/20.0
            ax1x_ang = (op_cls.__pg_joys_obj.get_axis(3)+_jb)/10.0
            ax1y_ang = (op_cls.__pg_joys_obj.get_axis(4)+_jb)/10.0
            ax2t_ang = (op_cls.__pg_joys_obj.get_axis(5)+_jb)/5.0
            """
            ax0x_ang = (op_cls.__pg_joys_obj.get_axis(bpy.context.scene.ax0x)+_jb)/20.0
            ax0y_ang = (op_cls.__pg_joys_obj.get_axis(bpy.context.scene.ax0y)+_jb)/20.0
            ax1x_ang = (op_cls.__pg_joys_obj.get_axis(bpy.context.scene.ax1x)+_jb)/10.0
            ax1y_ang = (op_cls.__pg_joys_obj.get_axis(bpy.context.scene.ax1y)+_jb)/10.0

            if bpy.context.scene.ax_t0 != -1 :
                ax2t_ang = (op_cls.__pg_joys_obj.get_axis(bpy.context.scene.ax_t0)+_jb)/5.0
            else :
                ax2t_ang = ((op_cls.__pg_joys_obj.get_axis(bpy.context.scene.ax_t1)+_jb) - (op_cls.__pg_joys_obj.get_axis(bpy.context.scene.ax_t2))) /10.0

            #print(ax0x_ang)
            #print(ax0y_ang)
            #print(ax1x_ang)
            #print(ax1y_ang)
            #print(ax2t_ang)

            #set transparent axis into viewport camera
            if context.space_data.__class__.__name__ == "SpaceView3D":
                v3d = context.space_data
                vp_infos = context.space_data.region_3d
                rv3d = v3d.region_3d
                #print(vp_infos.view_location) #xyz
                #print(vp_infos.view_rotation) #quaternion wxyz
                vrot = rv3d.view_rotation
                
                #print(qtn.__class__.__name__)
                #print(qtn[0])

                # transparent xy (view port axis)(並行移動)
                if ax1x_ang > 0.001 or ax1x_ang < -0.001 or ax1y_ang > 0.001 or ax1y_ang < -0.001:
                    #bpy.ops.view3d.view_pan(type='PANLEFT')
                    tpv =  vrot @ Vector((ax1x_ang,ax1y_ang,0))
                    rv3d.view_location += tpv
                
                # zoomin/out
                if ax2t_ang > 0.001 or ax2t_ang < -0.001:
                    #rv3d.view_camera_zoom = 0.0
                    
                    rv3d.view_distance -= ax2t_ang
                    #print=("ZOOM")

                # pan xy (回転)
                if ax0x_ang > 0.001 or ax0x_ang < -0.001 or ax0y_ang > 0.001 or ax0y_ang < -0.001:
                    x = Vector((1,0,0))
                    y = Vector((0,1,0))
                    z = Vector((0,0,1))
                    rmaty = rv3d.view_matrix.Rotation(ax0x_ang, 4, z)
                    #rmatz = rv3d.view_matrix.Rotation(ax0x_ang, 4, vrot @ z)
                    #rmatx = rv3d.view_matrix.Rotation(ax0y_ang, 4, x)
                    #rmaty = rv3d.view_matrix.Rotation(ax0x_ang, 4, y)
                    l,r,s = rmaty.decompose()
                    vrot[:] = r @ vrot
                    # it will not correct in high angle
                    rmatx = rv3d.view_matrix.Rotation(ax0y_ang, 4, vrot @ x)
                    l,r,s = rmatx.decompose()
                    vrot[:] = r @ vrot



                '''#transparent (stick to world axis/ワールド座標のX,Y,Zをスティック各軸に対応させ増減します)
                if ax1x_ang > 0.001 or ax1x_ang < -0.001:
                    #bpy.ops.view3d.view_pan(type='T_LEFT')
                    v3d = context.space_data
                    rv3d = v3d.region_3d
                    rv3d.view_location.x += ax1x_ang
                    #print("TL")

                if ax1y_ang > 0.001 or ax1y_ang < -0.001:
                    #bpy.ops.view3d.view_pan(type='T_UP')
                    v3d = context.space_data
                    rv3d = v3d.region_3d
                    rv3d.view_location.y += ax1y_ang
                    #print("TU")
            #rotate
            if ax0x_ang > 0.001 or ax0x_ang < -0.001:
                bpy.ops.view3d.view_orbit(angle=ax0x_ang,type='ORBITRIGHT')
            if ax0y_ang > 0.001 or ax0y_ang < -0.001:
                bpy.ops.view3d.view_orbit(angle=ax0y_ang,type='ORBITDOWN')
                '''




            



        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        op_cls = J2V3D_OT_Joy2view3Dctrl

        if context.area.type == 'VIEW_3D':
            # [開始] ボタンが押された時の処理(パネルかどこかからオペレーターが呼び出されたとき)
            if not op_cls.is_running():
                #Initialize Joystick(still no setting stickIDs)
                if bpy.context.scene.stick_ID_int == -1:
                    return{'FINISHED'}
                pygame.init()
                pygame.joystick.init()
                op_cls.__pg_joys_obj = pygame.joystick.Joystick(bpy.context.scene.stick_ID_int)
                op_cls.__pg_joys_obj.init()
                # start MODAL mode
                self.__handle_add(context)
                print("J2V3D: Joystick入力受付を開始しました。")
                return {'RUNNING_MODAL'}
            # [終了] ボタンが押された時の処理
            else:
                # モーダルモードを終了
                self.__handle_remove(context)
                print("J2V3D: Joystick入力受付を終了しました。")
                return {'FINISHED'}
        else:
            return {'CANCELLED'}


# UI
class J2V3D_PT_Joy2view3Dctrl(bpy.types.Panel):

    bl_label = "Joy2View_launch_pnl"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Joy2View"
    # bl_context = "objectmode"
    

    def draw(self, context):
        op_cls = J2V3D_OT_Joy2view3Dctrl
        scene = context.scene
        layout = self.layout
        # [開始] / [停止] ボタンを追加
        if not op_cls.is_running():
            # 第一変数のidnameのオペレーターを実行開始/停止するボタン
            layout.operator(op_cls.bl_idname, text="Start(now:off)", icon="PLAY")
        else:
            # 第一変数のidnameのオペレーターを実行開始/停止するボタン
            layout.operator(op_cls.bl_idname, text="Stop input(now:active)", icon="PAUSE")

class J2V3D_PT_settings(bpy.types.Panel):

    bl_label = "Joy2View_customize_pnl"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Joy2View"
    # bl_context = "objectmode"
    

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.separator()

        layout.label(text="状態更新")
        row = layout.row(align=True)
        row.operator(J2V3D_OT_Inithprops.bl_idname, text="接続状態",icon="FILE_REFRESH")
        row.operator(J2V3D_OT_Refreshprops.bl_idname, text="軸の情報",icon="FILE_REFRESH")
        
        layout.prop(scene,"stick_ID_int", text = "コントローラーを選択")
    

        if bpy.context.scene.stick_ID_int != -1 :
            layout.label(text="axis assigin")
            layout.prop(scene,"ax0x", text = "回転軸x")
            layout.prop(scene,"ax0y", text = "回転軸y")
            layout.prop(scene,"ax1x", text = "並行移動軸x")
            layout.prop(scene,"ax1y", text = "並行移動軸y")
            layout.prop(scene,"ax_t0", text = "ズーム軸(1軸)_-1で無効化")
            layout.prop(scene,"ax_t1", text = "ズーム軸(トリガー1)")
            layout.prop(scene,"ax_t2", text = "ズーム軸(トリガー2)")

            layout.separator()
            layout.label(text="key assigin")

class J2V3D_OT_Inithprops(bpy.types.Operator):
    # idnameには.を最低限一つ
    bl_idname = "view3d.joy2view_init_props"
    bl_label = "Joy2View_relesh"
    bl_description = "入力装置を更新します"

    def invoke(self, context, event):
        init_props()
        return {'FINISHED'}

class J2V3D_OT_Refreshprops(bpy.types.Operator):
    # idnameには.を最低限一つ
    bl_idname = "view3d.joy2view_refresh_props"
    bl_label = "Joy2View_relesh"
    bl_description = "軸情報を更新します"

    def invoke(self, context, event):
        ref_props()
        return {'FINISHED'}




from bpy.props import (
    IntProperty,
)


def init_props():
    
    pygame.init()
    pygame.joystick.init()
    sticks_num = pygame.joystick.get_count()
    pygame.quit()

    scene = bpy.types.Scene
    scene.stick_ID_int = IntProperty(
        name = 'joystick ID',
        default = 0,
        min = -1,
        max = sticks_num - 1
    )
    scene.ax0x = IntProperty(
        name = 'primalystick(x) ID',
        default = 0,
        min = 0,
        max = 5
    )
    scene.ax0y = IntProperty(
        name = 'primalystick(y) ID',
        default = 1,
        min = 0,
        max = 5
    )
    scene.ax1x = IntProperty(
        name = 'substick(x) ID',
        default = 3,
        min = 0,
        max = 5
    )
    scene.ax1y = IntProperty(
        name = 'substick(y) ID',
        default = 4,
        min = 0,
        max = 5
    )
    scene.ax_t0 = IntProperty(
        name = 'zoom axis ID',
        default = 5,
        min = -1,
        max = 5
    )
    scene.ax_t1 = IntProperty(
        name = 'zoomaxis ID',
        default = 5,
        min = 0,
        max = 5
    )
    scene.ax_t2 = IntProperty(
        name = 'zommaxis ID(optimal)',
        default = 0,
        min = 0,
        max = 5
    )

def ref_props():
    pygame.init()
    pygame.joystick.init()
    scene = bpy.types.Scene

    stick = pygame.joystick.Joystick(bpy.context.scene.stick_ID_int)
    stick.init()
    num_axes = stick.get_numaxes()
    pygame.quit()
    scene.ax0x = IntProperty(
        name = 'primalystick(x) ID',
        default = 0,
        min = 0,
        max = num_axes-1
    )
    scene.ax0y = IntProperty(
        name = 'primalystick(y) ID',
        default = 1,
        min = 0,
        max = num_axes-1
    )
    scene.ax1x = IntProperty(
        name = 'substick(x) ID',
        default = 3,
        min = 0,
        max = num_axes-1
    )
    scene.ax1y = IntProperty(
        name = 'substick(y) ID',
        default = 4,
        min = 0,
        max = num_axes-1
    )
    scene.ax_t0 = IntProperty(
        name = 'zoom axis ID',
        default = 5,
        min = -1,
        max = num_axes-1
    )
    scene.ax_t1 = IntProperty(
        name = 'trigger(zoom)1 ID',
        default = 0,
        min = 0,
        max = num_axes-1
    )
    scene.ax_t2 = IntProperty(
        name = 'trigger(zoom)2 ID',
        default = 0,
        min = 0,
        max = num_axes-1
    )



def clear_props():
    scene = bpy.types.Scene
    del scene.stick_ID_int
    del scene.ax0x
    del scene.ax0y
    del scene.ax1x
    del scene.ax1y
    del scene.ax_t0
    del scene.ax_t1
    del scene.ax_t2