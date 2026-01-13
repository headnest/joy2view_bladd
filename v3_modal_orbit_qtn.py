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

        # パネル [日時を表示] のボタン [終了] を押したときに、モーダルモードを終了
        if not self.is_running():
            # テキストオブジェクトを削除
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
            ax0x_ang = (op_cls.__pg_joys_obj.get_axis(0)+_jb)/20.0
            ax0y_ang = (op_cls.__pg_joys_obj.get_axis(1)+_jb)/20.0
            ax1x_ang = (op_cls.__pg_joys_obj.get_axis(3)+_jb)/10.0
            ax1y_ang = (op_cls.__pg_joys_obj.get_axis(4)+_jb)/10.0
            ax2t_ang = (op_cls.__pg_joys_obj.get_axis(5)+_jb)/5.0
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

                # transparent xy (view port axis)
                if ax1x_ang > 0.001 or ax1x_ang < -0.001 or ax1y_ang > 0.001 or ax1y_ang < -0.001:
                    #bpy.ops.view3d.view_pan(type='PANLEFT')
                    tpv =  vrot @ Vector((ax1x_ang,ax1y_ang,0))
                    rv3d.view_location += tpv
                
                # zoomin/out
                if ax2t_ang > 0.001 or ax2t_ang < -0.001:
                    #rv3d.view_camera_zoom = 0.0
                    
                    rv3d.view_distance -= ax2t_ang
                    #print=("ZOOM")

                # pan xy 
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



                '''#transparent (stick to world axis)
                if ax1x_ang > 0.001 or ax1x_ang < -0.001:
                    #bpy.ops.view3d.view_pan(type='PANLEFT')
                    v3d = context.space_data
                    rv3d = v3d.region_3d
                    rv3d.view_location.x += ax1x_ang
                    #print("PL")

                if ax1y_ang > 0.001 or ax1y_ang < -0.001:
                    #bpy.ops.view3d.view_pan(type='PANUP')
                    v3d = context.space_data
                    rv3d = v3d.region_3d
                    rv3d.view_location.y += ax1y_ang
                    #print("PU")
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
            # [開始] ボタンが押された時の処理
            if not op_cls.is_running():
                #Initialize Joystick(still no setting stickIDs)
                pygame.init()
                pygame.joystick.init()
                op_cls.__pg_joys_obj = pygame.joystick.Joystick(1)
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

    bl_label = "Joy2View_customize_pnl"
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
            layout.operator(op_cls.bl_idname, text="Start(now:off)", icon="PLAY")
        else:
            layout.operator(op_cls.bl_idname, text="Stop input(now:active)", icon="PAUSE")
        layout.separator()
        layout.prop(scene,"stick_ID_int", text = "コントローラーを選択")
        if bpy.context.scene.stick_ID_int != -1 :
            layout.label(text="axis assigin")



            layout.separator()
            layout.label(text="key assigin")


classes = [
    J2V3D_OT_Joy2view3Dctrl,
    J2V3D_PT_Joy2view3Dctrl,
]


from bpy.props import (
    IntProperty,
    BoolProperty,
    EnumProperty,
)


def init_props():
    sticks_num = pygame.joystick.get_count()
    pygame.init()
    pygame.joystick.init()
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
        default = 0,
        min = 0,
        max = 5
    )
    scene.ax1x = IntProperty(
        name = 'substick(x) ID',
        default = 0,
        min = 0,
        max = 5
    )
    scene.ax1y = IntProperty(
        name = 'substick(y) ID',
        default = 0,
        min = 0,
        max = 5
    )
    scene.ax_t1 = IntProperty(
        name = 'trigger ID',
        default = 0,
        min = 0,
        max = 5
    )
    scene.ax_t2 = IntProperty(
        name = 'trigger ID(optimal)',
        default = 0,
        min = 0,
        max = 5
    )
    pygame.quit()


def clear_props():
    scene = bpy.types.Scene
    del scene.stick_ID_int
    del scene.stick_ID_enum