---vertex
$HEADER$

attribute vec3 vColor;

void main(void)
{
    frag_color = vec4(vColor.rgb, 1.0);
    vec4 pos = vec4(vPosition.xy, 0.0, 1.0);
    gl_Position = projection_mat * modelview_mat * pos;
}

---fragment
$HEADER$

void main(void)
{
    gl_FragColor = frag_color;
}
