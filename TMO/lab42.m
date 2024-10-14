function [mean_matrix, var_matrix] = matrix_operations(I, J)
  vector_column = rand(I, 1);

  vector_row = rand(1, J); 

  result = vector_column * vector_row;

  mean_matrix = mean(result(:));

  var_matrix = var(result(:));
end

I = 15;
J = 25;

[mean_result, var_result] = matrix_operations(I, J);

disp(['Среднее значение матрицы: ', num2str(mean_result)]);
disp(['Дисперсия матрицы: ', num2str(var_result)]);