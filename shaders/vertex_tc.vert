#version 410 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;

out vec3 WorldPos_CS_in;
out vec3 Normal_CS_in;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    mat4 modelView = view * model;

    WorldPos_CS_in = vec3(model * vec4(aPos, 1.0));
    Normal_CS_in = mat3(transpose(inverse(model))) * aNormal;
}