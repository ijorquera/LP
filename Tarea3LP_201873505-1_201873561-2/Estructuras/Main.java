class Main{
    static public void main(String [] args){
        //Lectura de archivo:
        Scanner input = new Scanner(System.in);

        //lectura de archivo mapa.txt
        File file = new File(archive_1);
        input = new Scanner(file);
        //primera linea - nNodes, segunda - nEdges, adelante: u v w;
        int n = input.nextInt();
        int e = input.nextInt();
        Pais graph = new Pais(n,e);
        while(input.hasNextLine()) {
            int u = input.nextInt();
            int v = input.nextInt();
            int w = input.nextInt();
            graph.addEdge(u, v, w);
        }
        input.close();

        //lectura de archivo edificaciones.txt
        file = new File(archive_2);
        input = new Scanner(file);
        //ciudad casas edificios
        //consumo de cada casa
        //consumo de cada edificio
        while(input.hasNextLine()){

        }
        input.close();

        file = new File(archive_3);
        input = new Scanner(file);
        //precio balon de gas
        //precio litro de gas
        //costo por kilometro
        int balon = input.nextInt();
        int litro = input.nextInt();
        int costoKm = input.nextInt();
        input.close();
    }
}

//clase para guardar nombres de archivos, analogo de define
//dato freak: #define no existe en java porque no hay un pre-compilador
public class Constants {
    public static final String archive_1 = "mapa.txt";
    public static final String archive_2 = "edificaciones.txt";
    public static final String archive_3 = "empresa.txt";
}
