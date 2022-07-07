import re
import requests
import json

genome = "mm39"
chromosomes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', 'X', 'Y']

def find_sequence(genome_sequence):

    index_occurrences = [m.start() for m in re.finditer('(?=CACCTGC)', genome_sequence)]

    filtered_occurrences = []
    for index in index_occurrences:
        if (genome_sequence[int(index+11): int(index+15)] == "GCCT" or genome_sequence[int(index+11): int(index+15)] == "TGTT"):
            filtered_occurrences.append(index)
    return (index_occurrences, filtered_occurrences)

def main(): 
    for chromosome in chromosomes:
        data = requests.get('https://api.genome.ucsc.edu/getData/sequence?genome=' + genome +';chrom=chr' + chromosome).text
        parsed_data = json.loads(data)

        genome_sequence = parsed_data['dna'].upper()
        index_data = find_sequence(genome_sequence)

        text_file = open("/Users/marieyu/Desktop/projects/sequence_identifier/analyzed_sequences/" + genome +"-chr" + chromosome + ".txt", "w")
        n = text_file.write(
            'Genome:' + genome + " Chromosome: " + chromosome + 
            "\nCACCTGC occurrences: " + str(len(index_data[0])) + " occurrences\n[ " + " ,".join(map(str, index_data[0])) + " ]\n" +
            "\nCACCTGC....GCCT or CACCTGC....TGTT occurrences: "+ str(len(index_data[1])) + " occurrences\n[ " + " ,".join(map(str, index_data[1])) + " ]")
        text_file.close()

if __name__ == "__main__":
    main()


