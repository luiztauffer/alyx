-- Find the first three days each monkey saw each Y maze environment

select * 
from 
( 
	select subject, session_date, env_name, 
	row_number() over(partition by subject, env_name order by session_date) session_seq	
	from 
	( 
		select ssubj.nickname subject, date(asess.start_time) session_date, environments.env_name 
		from 
		buffalo_sessiontask bst, buffalo_buffalosession bsess, actions_session asess, 
		buffalo_task btask, subjects_subject ssubj, 
		( 
			select 
				case 
					when trim(lower(task)) ~ '^ymaze$' then lower(trim(task)) -- This don't replace the ymaze task
					when trim(lower(task)) ~ '^ymaze'	then regexp_replace(lower(regexp_replace(trim(task), '\mymaze', '', 'gi')), '[\s+]', '', 'g') -- This remove ymaze word from the task name
				end as env_name, 
				task_id 
			from ( 
				select btask.name task, btask.id task_id 
				from 
				buffalo_taskcategory btc, buffalo_task btask
				where 
				lower(btc.name) = 'ymaze' 
				and btc.id = btask.category_id 
			) env_clean 
		) environments 
		where 
		btask.id = environments.task_id 
		and btask.id = bst.task_id 
		and asess.id = bsess.session_ptr_id 
		and bsess.session_ptr_id = bst.session_id 
		and ssubj.id = asess.subject_id 
		group by ssubj.nickname, environments.env_name, date(asess.start_time) 
		order by ssubj.nickname, environments.env_name, date(asess.start_time) 
	) env_logs 
) env_logs_filtered 
where env_logs_filtered.session_seq <= 3 
and env_logs_filtered.subject = 'test' -- Update this nickname
