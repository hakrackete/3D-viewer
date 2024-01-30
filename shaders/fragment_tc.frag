#version 410 core
                                                               
in vec3 Normal_FS_in;                                                                       
in vec3 WorldPos_FS_in;
uniform int illuminate_everything;
uniform vec3 cam_pos;

out vec4 FragColor;

void main() {
    // Direkt festgelegte Lichtposition
    if (illuminate_everything == 0){
        vec3 lightPos = vec3(0.0, 5.0, 5.0);

        // Calculate lighting (simple diffuse lighting)
        vec3 norm = normalize(Normal_FS_in);
        vec3 lightDir = normalize(lightPos - WorldPos_FS_in);
        float diff = max(dot(norm, lightDir), 0.0);
        vec3 diffuse = diff * vec3(1.0, 1.0, 1.0);  // Festgelegte Lichtfarbe (weiß)
        float ambient = 0.1;

        vec3 V = normalize(cam_pos - WorldPos_FS_in);
        vec3 R = normalize(2* dot(norm,lightDir) * norm - lightDir);

        float specular = pow(dot(R,V),10);
        float specular_intensity = 0.5;

        // Final color calculation
        vec3 objectColor = vec3(1.0, 0.5, 0.2);  // Beispielobjektfarbe (orange)
        vec3 result =  1.2 * objectColor * diffuse + objectColor * ambient + specular_intensity * specular * vec3(1.0);
        FragColor = vec4(result, 1.0);

    }else{
        FragColor = vec4(1.0);
    }
}