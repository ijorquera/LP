import java.util.ArrayList;
import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;

//clase para guardar nombres de archivos, analogo de define
//dato freak: #define no existe en java porque no hay un pre-compilador
class Constants {
    public static final String archive_1 = "mapa.txt";
    public static final String archive_2 = "edificaciones.txt";
    public static final String archive_3 = "empresa.txt";
}

class Main{
    static public void main(String [] args){
        //Lectura de archivo (usando clase Scanner)
        Scanner input = new Scanner(System.in);
        Pais graph = null;

        //lectura de archivo mapa.txt
        File file = new File(Constants.archive_1);
        try{
            input = new Scanner(file);
            //primera linea - nNodes, segunda - nEdges, adelante: u v w;
            int n = input.nextInt();
            int e = input.nextInt();
            graph = new Pais(n,e);
            while(input.hasNextLine()) {
                int u = input.nextInt();
                int v = input.nextInt();
                int w = input.nextInt();
                graph.addEdge(u, v, w);
            }
            input.close();
        }
        catch(FileNotFoundException e){
            System.out.println("Error en apertura de archivo " + file +".");
            e.printStackTrace();
        }
        //lectura de archivo edificaciones.txt
        file = new File(Constants.archive_2);
        try{
            input = new Scanner(file);
            //ciudad casas edificios
            //consumo de cada casa
            //consumo de cada edificio
            //aqui queremos leer de a 3 lineas.
            while(input.hasNextLine()){
                int idCiudad = input.nextInt();
                int nCasas = input.nextInt();
                int nEdificios = input.nextInt();
                Ciudad c = new Ciudad(nCasas,nEdificios);


                //crear cosas con casas y edificios
                for(int i = 0; i < nCasas; i++){
                    int consumo = input.nextInt();
                    Casa ca = new Casa(consumo);
                    c.addEdificacion(ca);
                }
                for(int i = 0; i < nEdificios; i++){
                    int consumo = input.nextInt();
                    Edificio edi = new Edificio(consumo);
                    c.addEdificacion(edi);

                }
                //finalmente, agrego ciudad al pais.
                graph.addNode(idCiudad, c);
            }
            input.close();
        }
        catch(FileNotFoundException e){
            System.out.println("Error en apertura de archivo " + file +".");
        }

        file = new File(Constants.archive_3);
        try{
            input = new Scanner(file);
            //Formato de archivo: (solo 3 lineas)
            //precio balon de gas
            //precio litro de gas
            //costo por kilometro
            int balon = input.nextInt();
            int litro = input.nextInt();
            int costoKm = input.nextInt();
            Empresa empresa = new Empresa(balon, litro, costoKm);
            input.close();
        }
        catch(FileNotFoundException e){
            System.out.println("Error en apertura de archivo " + file +".");
        }
    }
}
