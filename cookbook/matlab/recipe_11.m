username = 'database_user';
password = '';
datasource = "alyx";
conn = postgresql(datasource,username,password);

% Get data from electrodes x,y,z

% Set this variable with the text you wanna search
subject_nickname = 'monita3'
% Set this variables with the intial and final date of the date range you want to query
date = '2019-12-10'

% 'where be.channel_number in (''36'', ''5'')  ' ... replace the numbers
% with the channel numbers you want to query

electrodes_query = sprintf(['select distinct  be2.turn, be2.impedance , be2.notes, be2.date_time, bc.notes, bc.number_of_cells, bc.ripples, b4.channel_number '  ...
'from buffalo_channelrecording bc, buffalo_electrodelog be2, ( ' ...
'select id, be.channel_number ' ...
'from buffalo_electrode be ' ...
'where be.channel_number in (''36'', ''5'')  ' ...
'and be.subject_id = ( ' ...
'select id from subjects_subject ss where ss.nickname=''%s'' ) ' ...
') b4 ' ...
'where be2.electrode_id in (b4.id) ' ...
'and date(be2.date_time) = ''%s'' ' ...
'and bc.electrode_id in (b4.id) ' ...
'order by be2.date_time' ...
], subject_nickname, date)

electrodes_data = fetch(conn, electrodes_query);