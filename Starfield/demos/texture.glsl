---vertex
$HEADER$

void main(void)
{
    tex_coord0 = vTexCoords0;
    vec4 pos = vec4(vPosition.xy, 0.0, 1.0);
    gl_Position = projection_mat * modelview_mat * pos;
}

---fragment
$HEADER$

void main(void)
{
    gl_FragColor = texture2D(texture0, tex_coord0);
}
