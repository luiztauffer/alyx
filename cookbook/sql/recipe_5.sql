-- Tell me which wires have had cells in the last week but do not today

select be.channel_number 
from buffalo_device bd, buffalo_electrode be, 
buffalo_buffalosubject bsub, buffalo_buffalosession bsess, 
actions_session asess, buffalo_channelrecording bch, subjects_subject ssub 
where 
ssub.nickname = 'snake' -- Update this nickname
and ssub.id = bsub.subject_ptr_id 
and asess.id = bsess.session_ptr_id 
and bsess.session_ptr_id = bch.session_id 
and (bch.number_of_cells = '3' or bch.number_of_cells = '4') 
and bsub.subject_ptr_id = bd.subject_id 
and bd.id = be.device_id 
and be.id = bch.electrode_id 
and date(asess.start_time) >= date_trunc('week', now())::date - 7 
and date(asess.start_time) <= date_trunc('week', now())::date - 1 
and be.channel_number not in ( 
	select be_s.channel_number 
	from buffalo_device bd_s, buffalo_electrode be_s, 
	buffalo_buffalosubject bsub_s, buffalo_buffalosession bsess_s, 
	actions_session asess_s, buffalo_channelrecording bch_s 
	where 
	bsub_s.subject_ptr_id = bsub.subject_ptr_id 
	and asess_s.id = bsess_s.session_ptr_id 
	and bsess_s.session_ptr_id = bch_s.session_id 
	and (bch_s.number_of_cells = '3' or bch_s.number_of_cells = '4') 
	and bsub_s.subject_ptr_id = bd_s.subject_id 
	and bd_s.id = be_s.device_id 
	and be_s.id = bch_s.electrode_id 
	and date(asess_s.start_time) = current_date 
) 
group by be.channel_number
