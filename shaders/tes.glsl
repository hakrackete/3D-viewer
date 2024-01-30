// Tesselation Code by Ogldev https://ogldev.org/www/tutorial31/tutorial31.html
#version 410 core                                                                               
                                                                                             
layout(triangles, equal_spacing, ccw) in;                                                       
                                                                                                 
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;     
uniform float PN_factor; 
uniform float smooth_shade;                                                                    
                                                                                                
struct OutputPatch                                                                              
{                                                                                               
    vec3 WorldPos_B030;                                                                         
    vec3 WorldPos_B021;                                                                         
    vec3 WorldPos_B012;                                                                         
    vec3 WorldPos_B003;                                                                         
    vec3 WorldPos_B102;                                                                         
    vec3 WorldPos_B201;                                                                         
    vec3 WorldPos_B300;                                                                         
    vec3 WorldPos_B210;                                                                         
    vec3 WorldPos_B120;                                                                         
    vec3 WorldPos_B111;                                                                         
    vec3 Normal[3];
    vec3 Normal_110;
    vec3 Normal_011;
    vec3 Normal_101;                                                                                                                                         
};                                                                                        
                                                                                                
in patch OutputPatch oPatch;                                                                    
                                                                                                
out vec3 WorldPos_FS_in;                                                                        
                                                                       
out vec3 Normal_FS_in;                                                                          
                                                                                                
vec2 interpolate2D(vec2 v0, vec2 v1, vec2 v2)                                                   
{                                                                                               
    return vec2(gl_TessCoord.x) * v0 + vec2(gl_TessCoord.y) * v1 + vec2(gl_TessCoord.z) * v2;   
}                                                                                               
                                                                                                
vec3 interpolate3D(vec3 v0, vec3 v1, vec3 v2)                                                   
{                                                                                               
    return vec3(gl_TessCoord.x) * v0 + vec3(gl_TessCoord.y) * v1 + vec3(gl_TessCoord.z) * v2;   
}
vec3 flatshade(vec3 v0, vec3 v1, vec3 v2)
{
    return vec3(0.33) * v0 + vec3(0.33) * v1 + vec3(0.33) * v2;   
}                                                                                          
                                                                                                
void main()                                                                                     
{                                                                                               
    // Interpolate the attributes of the output vertex using the barycentric coordinates        

    if (smooth_shade == 1){
        Normal_FS_in = interpolate3D(oPatch.Normal[0], oPatch.Normal[1], oPatch.Normal[2]);  
    }
    else{
        Normal_FS_in = flatshade(oPatch.Normal[0], oPatch.Normal[1], oPatch.Normal[2]);
    }

    // gl_TessCoord sind die Baryzentrischen Koordinaten die vom Tesselator als Punkte evaluiert wurden
    float u = gl_TessCoord.x;                                                                   
    float v = gl_TessCoord.y;                                                                   
    float w = gl_TessCoord.z;                                                                   
    float uPow3 = pow(u, 3);                                                                    
    float vPow3 = pow(v, 3);                                                                    
    float wPow3 = pow(w, 3);                                                                    
    float uPow2 = pow(u, 2);                                                                    
    float vPow2 = pow(v, 2);                                                                    
    float wPow2 = pow(w, 2);

    vec3 FlatTrianglePos_FS_in = oPatch.WorldPos_B300 * w + oPatch.WorldPos_B030 * u + oPatch.WorldPos_B003 * v;

    // alternative Arten das Dreieck zu berechnen, führt zu lustigen effekten bei der interpolation
    // vec3 FlatTrianglePos_FS_in = oPatch.WorldPos_B300 * u + oPatch.WorldPos_B030 * v + oPatch.WorldPos_B003 * w;
    // vec3 FlatTrianglePos_FS_in = oPatch.WorldPos_B300 * u + oPatch.WorldPos_B030 * w + oPatch.WorldPos_B003 * v;


    WorldPos_FS_in = oPatch.WorldPos_B300 * wPow3 + oPatch.WorldPos_B030 * uPow3 + oPatch.WorldPos_B003 * vPow3 +                               
                     oPatch.WorldPos_B210 * 3.0 * wPow2 * u + oPatch.WorldPos_B120 * 3.0 * w * uPow2 + oPatch.WorldPos_B201 * 3.0 * wPow2 * v + 
                     oPatch.WorldPos_B021 * 3.0 * uPow2 * v + oPatch.WorldPos_B102 * 3.0 * w * vPow2 + oPatch.WorldPos_B012 * 3.0 * u * vPow2 + 
                     oPatch.WorldPos_B111 * 6.0 * w * u * v;  

    WorldPos_FS_in = PN_factor * WorldPos_FS_in + (1-PN_factor) * FlatTrianglePos_FS_in; 
    mat4 gVP = projection * view;                               
    gl_Position = gVP * vec4(WorldPos_FS_in, 1.0);                                              
}                                                                                               
