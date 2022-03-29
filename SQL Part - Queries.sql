-- Q1.a+b:
select d.name, e.first_name, e.last_name, e.salary
	from employees e join departments d
						on e.department_id = d.id
	where (e.department_id, e.salary) in (select department_id, max(salary) over (partition by department_id) from employees);

-- Q1.c:
select department_name, top_salary-second_salary as salary_diff from (
	select distinct d.name as department_name, nth_value(e.salary,1) over (partition by d.name order by salary desc) as top_salary,
	nth_value(e.salary,2) over (partition by d.name order by salary desc 
	RANGE BETWEEN
	UNBOUNDED PRECEDING AND
	UNBOUNDED FOLLOWING) as second_salary
	from employees e join departments d
				on e.department_id = d.id)a;

-- If you meant to write one query
-- Q1:
select * from
(select e.department_id, d.name as department_name,
       concat(e.first_name, ' ', e.last_name) as employee_name,
       e.salary,
       row_number() over(partition by e.department_id order by e.salary desc) as top_salary,
       e.salary - lead(e.salary, 1) over(partition by e.department_id order by e.salary desc) as salary_diff
       from employees e join departments d on e.department_id = d.id)a
where top_salary = 1
order by department_id;

-- Q2:
select concat(round((sum(case when datediff(CURDATE(),hire_date) > 3*365 then 1 else 0 end)*100 / count(*)),2), '%')
		as 'Employees_Working_More_Than_3_Years[%]'
from employees;