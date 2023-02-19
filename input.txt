int numero, n1, n2;
real m;
int fatorial (int fat){
if (fat > 1){
print (fat);
return fat * fatorial(fat - 1);
} else {
return 1;
}
}
mostrarMedia (int v1, int v2, real x){
x = (v1+v2)/2;
print ("Resultado: ", x);
}
real media (real n1, real n2)
{
real m;
m = (n1 + n2)/2;
return m;
}
main(){
print ("Programa Fatorial. Digite o valor?");
input(numero);
print(fatorial(numero));
print ("Programa Media. Digite o valores?");
input(n1, n2);
print(mostrarMedia(n1, n2, m));
}