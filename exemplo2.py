int max; 
real n1, n2, m;
const real PI=3.14;
String ies;

main(){
    int i, j, mes;
    print("Programa media de dois numeros: ");
    input(n1, n2);
    m = (n1+n2)/2;
    print("Media: ", m);
    for (i=0; i<max; i=i+1) {
        for (j=0; j<max; j=j-1) {
            if (i==j) {
                print("Diagonal principal");
            } else {
            if (i>j) {
                print("Acima da diagonal");
            }
            else {
                print("Abaixo da diagonal");
            }
            }
        }
    }
    input(mes);
    while (mes <= 0 && mes > 12) {
        print("Mes invalido");
        input(mes);
        if (mes <= 12){
            print("mes valido");
        }
    }
}