#version 410 core
in vec3 FragPos;
in vec3 Normal;

out vec4 FragColor;

void main() {
    // Direkt festgelegte Lichtposition
    vec3 lightPos = vec3(0.0, 5.0, 5.0);

    // Calculate lighting (simple diffuse lighting)
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * vec3(1.0, 1.0, 1.0);  // Festgelegte Lichtfarbe (weiß)
    float ambient = 0.1;

    // Final color calculation
    vec3 objectColor = vec3(1.0, 0.5, 0.2);  // Beispielobjektfarbe (orange)
    vec3 result = objectColor * diffuse + objectColor * ambient;
    FragColor = vec4(result, 1.0);
}