#include "header.h"

void process_file(const char *input_filename, const char *output_filename) {
    FILE *input_file = fopen(input_filename, "r");
    FILE *output_file = fopen(output_filename, "w");

    if (input_file == NULL) {
        perror("fopen input");
        exit(EXIT_FAILURE);
    }

    if (output_file == NULL) {
        perror("fopen output");
        exit(EXIT_FAILURE);
    }
    
    double average_grade = 0;
    int num_students = 0;
    char student_name[BUFFER_SIZE];
    int group_number;
    int grade1, grade2, grade3;


    while (fscanf(input_file, "%s %d %d %d %d", student_name, &group_number, &grade1, &grade2, &grade3) == 5) {
        if (grade1 < 4 || grade2 < 4 || grade3 < 4) {
          fprintf(output_file, "%s %d\n", student_name, (grade1 < 4) + (grade2 < 4) + (grade3 < 4)); 
        }
    }

    fclose(input_file);
    fclose(output_file);
}