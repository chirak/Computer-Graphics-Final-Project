float4x4 xWorldViewProjection;

Texture xColoredTexture;

sampler ColoredTextureSampler = sampler_state
{ texture = <xColoredTexture> ;
magfilter = LINEAR; minfilter = LINEAR; mipfilter=LINEAR;
AddressU = mirror; AddressV = mirror;};

struct VertexIn
{
    float4 position : POSITION;
    float2 textureCoordinates : TEXCOORD0;
};

struct VertexOut
{
    float4 Position : POSITION;
    float2 textureCoordinates : TEXCOORD0;
};

VertexOut VertexShaderFunction(VertexIn input)
{
    VertexOut Output = (VertexOut)0;
    Output.Position =mul(input.position, xWorldViewProjection);
    Output.textureCoordinates = input.textureCoordinates;

    return Output;
}

float4 PixelShaderFunction(VertexOut input) : COLOR0
{
    float4 Color;
    Color =  tex2D(ColoredTextureSampler, input.textureCoordinates.xy);
    Color += tex2D(ColoredTextureSampler, input.textureCoordinates.xy + (0.01));
    Color += tex2D(ColoredTextureSampler, input.textureCoordinates.xy - (0.01));
    Color = Color / 3;

    return Color;
}

technique Textured
{
    pass Pass0
    {
        VertexShader = compile vs_2_0 VertexShaderFunction(  );
        PixelShader = compile ps_2_0 PixelShaderFunction(  );
    }
}