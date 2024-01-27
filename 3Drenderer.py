import glfw
from OpenGL.GL import *
import pyassimp
import glm
import ctypes
from pygame import time


model_path = 'models/susanne.obj'
window_width = 800
window_height = 600


clock = time.Clock()


view_matrix = glm.mat4(1.0)


tessellation_level = 1.0  # Setze hier den gewünschten Wert

wireframemode = False
illuminate_everything = 0
smooth_shade = 1

PN_factor = 1


vertex_shader = open("./shaders/vertex_tc.vert","r").read()
fragment_shader = open("./shaders/fragment_tc.frag","r").read()
tc_shader = open("./shaders/tcs.glsl","r")
te_shader = open("./shaders/tes.glsl","r")

def check_gl_error():
    err = glGetError()
    if err != GL_NO_ERROR:
        raise Exception(f"OpenGL error: {err}")



def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)



    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise Exception("Shader compilation failed: " + glGetShaderInfoLog(shader).decode())

    return shader

def compile_shader_program(vertex_source, fragment_source,tcontrol_source,tevaluation_source):
    vertex_shader_compiled = compile_shader(vertex_source, GL_VERTEX_SHADER)
    fragment_shader_compiled = compile_shader(fragment_source, GL_FRAGMENT_SHADER)
    tc_compiled = compile_shader(tcontrol_source,GL_TESS_CONTROL_SHADER)
    te_compiled = compile_shader(tevaluation_source,GL_TESS_EVALUATION_SHADER)

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader_compiled)
    glAttachShader(shader_program, tc_compiled)
    glAttachShader(shader_program, te_compiled)
    glAttachShader(shader_program, fragment_shader_compiled)

    check_gl_error()
    glLinkProgram(shader_program)
    check_gl_error()

    glValidateProgram(shader_program)

    if not glGetProgramiv(shader_program, GL_LINK_STATUS):
        raise Exception("Shader program linking failed: " + glGetProgramInfoLog(shader_program).decode())

    glDeleteShader(vertex_shader_compiled)
    glDeleteShader(tc_compiled)
    glDeleteShader(te_compiled)

    glDeleteShader(fragment_shader_compiled)

    return shader_program

def load_scene(file_path):
    with pyassimp.load(file_path) as scene:
        if not scene.meshes:
            raise ValueError(f"No meshes found in the scene loaded from {file_path}")

        vaos = []
        num_vertices_list = []

        for mesh in scene.meshes:
            vao = glGenVertexArrays(1)
            glBindVertexArray(vao)

            vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, vbo)

            interleaved_data = []
            for i in range(len(mesh.vertices)):
                interleaved_data.extend(mesh.vertices[i])
                interleaved_data.extend(mesh.normals[i])

            glBufferData(GL_ARRAY_BUFFER, (GLfloat * len(interleaved_data))(*interleaved_data), GL_STATIC_DRAW)

            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * ctypes.sizeof(GLfloat), None)
            glEnableVertexAttribArray(0)

            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * ctypes.sizeof(GLfloat), ctypes.c_void_p(3 * ctypes.sizeof(GLfloat)))
            glEnableVertexAttribArray(1)

            glBindVertexArray(0)
            glBindBuffer(GL_ARRAY_BUFFER, 0)

            vaos.append(vao)
            num_vertices_list.append(len(mesh.vertices))

        return vaos, num_vertices_list

def key_callback(window, key, scancode, action, mods):
    global wireframemode,illuminate_everything,wireframemode,PN_factor,smooth_shade
    if key == glfw.KEY_T and action == glfw.PRESS:
        wireframemode = not(wireframemode)
    if key == glfw.KEY_L and action == glfw.PRESS:
        illuminate_everything = 1 - illuminate_everything
    if key == glfw.KEY_F and action == glfw.PRESS:
        smooth_shade  = 1 - smooth_shade
    if key == glfw.KEY_H and action == glfw.PRESS:

        print(f"""
[1-9] choose Tesselation Level: {tessellation_level}
[T] toggle wireframe Modus: {wireframemode}
[L] illuminate Everything: {bool(illuminate_everything)}
[N,M] Scale the PN-Factor: {PN_factor}
[F] toggle between smooth and Flat shading: {smooth_shade}
[Arrow-Keys] change Rotation of the Model
[W,S] Zoom in/out 
[H] Print this Help screen""")

    

# Set the key callback function

def process_input(window):
    global view_matrix,tessellation_level,wireframemode,PN_factor
    scale_factor =1

    # Rotationsgeschwindigkeit
    rotation_speed = 0.07
    # Skalierungsgeschwindigkeit
    scaling_speed = 0.07

    PN_factor_speed = 0.07

    # Abfrage für Pfeiltasten (Rechts, Links, Hoch, Runter)
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        # Drehung nach rechts um die y-Achse
        view_matrix = glm.rotate(view_matrix, rotation_speed, glm.vec3(0.0, 1.0, 0.0))
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        # Drehung nach links um die y-Achse
        view_matrix = glm.rotate(view_matrix, -rotation_speed, glm.vec3(0.0, 1.0, 0.0))
    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        # Drehung nach oben um die x-Achse
        view_matrix = glm.rotate(view_matrix, -rotation_speed, glm.vec3(1.0, 0.0, 0.0))
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        # Drehung nach unten um die x-Achse
        view_matrix = glm.rotate(view_matrix, rotation_speed, glm.vec3(1.0, 0.0, 0.0))
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        # Skalierung nach vorne (verkleinern)
        scale_factor -= scaling_speed
        view_matrix = glm.scale(view_matrix, glm.vec3(scale_factor, scale_factor, scale_factor))
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        # Skalierung nach hinten (vergrößern)
        scale_factor += scaling_speed
        view_matrix = glm.scale(view_matrix, glm.vec3(scale_factor, scale_factor, scale_factor))
    

    if glfw.get_key(window, glfw.KEY_M) == glfw.PRESS:
        PN_factor += PN_factor_speed
    if glfw.get_key(window, glfw.KEY_N) == glfw.PRESS:
        PN_factor -= PN_factor_speed
    if glfw.get_key(window, glfw.KEY_R) == glfw.PRESS:
        PN_factor = 1
    
    # der PN faktor sorgt für die interpolation zwischen flachen Dreiecken und den tesselierten Dreiecken, hat nur didaktischen Wert
    # bitte nicht bei real-world anwendungen implementieren
    # diese Zeile auskommentiern um lustige effekte zu erzielen
    PN_factor = min(max(PN_factor,0),1)



    for i, key in enumerate(range(glfw.KEY_0, glfw.KEY_9 + 1)):
        if glfw.get_key(window, key) == glfw.PRESS:
            tessellation_level = float(i)
    

    
@GLDEBUGPROC
def debug_callback(source, type, id, severity, length, message, user_param):
    print(f"OpenGL Debug Message:")
    print(f"  Source: {source}")
    print(f"  Type: {type}")
    print(f"  ID: {id}")
    print(f"  Severity: {severity}")
    print(f"  Message: {message}")

def main():
    global view_matrix

    
    if not glfw.init():
        return

    glfw.window_hint(glfw.SAMPLES, 10)
    window = glfw.create_window(window_width, window_height, "3D Model Viewer", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)


    glfw.make_context_current(window)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)

    # glEnable(GL_CULL_FACE)
    # glCullFace(GL_BACK) 

    glEnable(GL_DEBUG_OUTPUT)
    glEnable(GL_DEBUG_OUTPUT_SYNCHRONOUS)
    glDebugMessageCallback(debug_callback, None)


    # Set up shaders
    shader_program = compile_shader_program(vertex_shader, fragment_shader,tc_shader,te_shader)

    # Set up uniform locations
    model_location = glGetUniformLocation(shader_program, "model")
    view_location = glGetUniformLocation(shader_program, "view")
    projection_location = glGetUniformLocation(shader_program, "projection")
    tessellation_level_location = glGetUniformLocation(shader_program, "gTessellationLevel")
    illuminate_everything_location = glGetUniformLocation(shader_program,"illuminate_everything")
    PN_factor_location = glGetUniformLocation(shader_program,"PN_factor")
    smooth_shade_location = glGetUniformLocation(shader_program,"smooth_shade")


    # Replace 'path/to/your/model.obj' with your actual model file path
    vaos, num_vertices_list = load_scene(model_path)

    # Set up initial values
    view_matrix = glm.lookAt(glm.vec3(0, 0, 3), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    projection_matrix = glm.perspective(glm.radians(45.0), window_width / window_height, 0.1, 100.0)

    glfw.set_key_callback(window, key_callback)


    while not glfw.window_should_close(window):
        if wireframemode:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)   
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        clock.tick(60)
        glfw.poll_events()

        process_input(window)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(shader_program)

        # Set up model, view, and projection matrices
        model_matrix = glm.mat4(1)
        glUniformMatrix4fv(model_location, 1, GL_FALSE, glm.value_ptr(model_matrix))
        glUniformMatrix4fv(view_location, 1, GL_FALSE, glm.value_ptr(view_matrix))
        glUniformMatrix4fv(projection_location, 1, GL_FALSE, glm.value_ptr(projection_matrix))
        glUniform1f(tessellation_level_location, tessellation_level)
        glUniform1i(illuminate_everything_location,illuminate_everything)
        glUniform1f(PN_factor_location,PN_factor)
        glUniform1f(smooth_shade_location,smooth_shade)

        for i,model_vao in enumerate(vaos):
            glBindVertexArray(model_vao)
            check_gl_error()

            glDrawArrays(GL_PATCHES, 0, num_vertices_list[i])
            # glDrawElements(GL_PATCHES,num_vertices,GL_UNSIGNED_INT,0)
            check_gl_error()


        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
