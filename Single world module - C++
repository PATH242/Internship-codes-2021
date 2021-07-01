#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <random>
#include <chrono>
#define f first
#define s second
#define LD long double
#define GNUPLOT_NAME "C:\\gnuplot\\bin\\gnuplot"
using namespace std;
///to ensure better randomness than rand()
mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());
#define rnd(s ,e) uniform_int_distribution<int>(s, e)(rng)

///the constants used
const int generationSize=10,probabilityOfMutation=20,probabilityOfMating=60,N=195,mutationValues[2]={1,-1};
int n,numberOfGenerations; ///n is size of the input array, numberOfGenerations is a counter to count the generations made so far
double e[N],d[N]; ///e[N] is an array for the errors going to be processed

class Individual{
public:
    pair<LD,LD> genes;
    LD fitness; ///fitness is the error value
    ///the lower the fitness the better
    ///genes represent the equation, genes.first + genes.second * x
    Individual(){
        for(int i=0;i<n;i++)
            genes= {rnd(0,40),rnd(0,40)};
        fitness= calculateFitness();
    }
    ///mating happens, then mutation, then fitness is calculated
    Individual mate(const Individual& temp) const{

        Individual child;
        child.genes= {(this->genes.f+temp.genes.f)/2.0, (this->genes.s+temp.genes.s)/2.0};
        child.mutate();
        child.fitness= child.calculateFitness();
        return child;
    }
    ///mutation happens with the probability of mutation specified above
    void mutate(){
        int probability;
        probability= (rnd(0,99));
        if(probability<probabilityOfMutation){
            genes.f+= mutationValues[rnd(0,1)]*rnd(0,10);
        }
        probability= (rnd(0,99));
        if(probability<probabilityOfMutation){
            genes.s+= mutationValues[rnd(0,1)]*rnd(0,10);
        }
    }

    ///fitness is the sum of [differences between expected e[i] and actual e[i] squared]
    LD calculateFitness(){
        LD temp, tempDif;
        for(int i=0;i<n;i++){
            tempDif= genes.f+ genes.s*d[i];
            tempDif-=e[i];
            temp+= (tempDif)*(tempDif);
        }
        return temp;
    }

    ///comparison operator that's used in sorting
    bool operator<(const Individual& right) const{
        return(this->fitness<right.fitness);
    }
    ///to output the class when needed
    friend ostream &operator<<(ostream& output, Individual& I){
        output<<I.genes.f<<' '<<I.genes.s<<" with fitness: "<<I.fitness<<' ';
        return output;
    }
};

vector<Individual> population;
///generating a random population
void makeInitialPopulation(){
    for(int i=0;i<generationSize;i++){
        Individual I;
        population.push_back(I);
    }
}


void selectAdvancedIndividuals(){
    ///sort to have least fit regression line first
    sort(population.begin(),population.end());
    reverse(population.begin(),population.end());
    ///create a new population for the children
    vector<Individual> newPopulation;
    Individual temp;
    int probability;
    ///mating with giving most similar lines higher probability in mating
    for(int i=(int)(population.size()-1);i>=0;i--){
        for(int j=i-1;j>=0;j--){
            probability= (rnd(0,99))+i*2;
            if(probability>=probabilityOfMating){
                temp= population[i].mate(population[j]);
                newPopulation.push_back(temp);
            }
        }
    }
    ///sort to have most fit regression line first
    sort(newPopulation.begin(),newPopulation.end());

    ///eliminate from the new population so that it suits the generation size
    while(newPopulation.size()>generationSize)
        newPopulation.pop_back();

    population= newPopulation;
}

///read data from file and represent it in arrays
void readData(){
    n=195;
    ifstream data;
    data.open("dataIN.txt");
    for(int i=0;i<n;i++)
        data>>e[i]>>d[i];
    data.close();

}
int main() {
    readData();
    makeInitialPopulation();

    for(int i=0;i<1e4;i++){
        numberOfGenerations++;
        selectAdvancedIndividuals();
        ///if we reach an optimal individual, break
        if(population[0].fitness <= 100)
            break;
    }

    FILE* pipe= NULL;
    FILE* fp= NULL;
    pipe = popen(GNUPLOT_NAME, "w");
    ///create our equation in a string to use it to plot the graph
    string s="";
    s+= to_string(population[0].genes.f);
    s+="*x**0+";
    s+=to_string(population[0].genes.s);
    s+="*x**1";

    s= "f(x)= "+s;
    ///output the equation and fitness
    cout<<s<<'\n';
    cout<<"total fitness is: "<<population[0].fitness<<'\n';

    ///represent the actual values and the regression line on a graph
    if(pipe != NULL){

        fprintf(pipe, "set term wx \n");         // set the terminal
        fprintf(pipe, "%s\n", s.c_str());
        fprintf(pipe, "%s\n", "plot f(x),'-' using 1:1 with points pt 20 ps 1");
        fprintf(pipe, "%s\n","plot '-' using 1:1 title 'polynomial' with points" );
        for(int i = 0; i < n; i++){
            fprintf(pipe, "%f\t%f\n", d[i],e[i]);
        }

    }

    return 0;
}
