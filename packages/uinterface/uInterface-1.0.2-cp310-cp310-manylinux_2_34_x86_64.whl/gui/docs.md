# uInterface module documentation

This is a description of the functions included in the uInterface library.

## get_problem(u16 num)

Gets a problem by using the number of the problem as the identificator. Returns a dictionary containing the following data:

``` Text
pid: Id of the problem,
num: Number of the problem,
title: Name of the problem,
dacu: Number of distinct accepted users,
mrun: Best time of an accepted problem,
mmem: Best memory usage of an accepted problem,
nover: Number of no veredicts,
sube: Number of submission error veredicts,
noj: Number of not judged veredicts,
inq: Number of in queue veredicts,
ce: Number of compilation error veredicts,
rf: Number of restricted function veredicts,
re: Number of runtime error veredicts,
ole: Number of output limit exceeded veredicts,
tle: Number of time limit exceeded veredicts,
mle: Number of memory limit exceeded veredicts,
wa: Number of wrong answer veredicts,
pe: Number of presentation error veredicts,
ac: Number of accepted veredicts,
rtl: Problem Run-Time limit,
status: Problem Status (0 = unavailable, 1 = normal, 2 = special judge) ,
```

## get_problem_pid(u16 pid)

Gets a problem by using the problem's id as the identificator. Returns a dictionary containing the following data:

``` Text
pid: Id of the problem,
num: Number of the problem,
title: Name of the problem,
dacu: Number of distinct accepted users,
mrun: Best time of an accepted problem,
mmem: Best memory usage of an accepted problem,
nover: Number of no verdicts,
sube: Number of submission error verdicts,
noj: Number of not judged verdicts,
inq: Number of in queue verdicts,
ce: Number of compilation error verdicts,
rf: Number of restricted function verdicts,
re: Number of runtime error verdicts,
ole: Number of output limit exceeded verdicts,
tle: Number of time limit exceeded verdicts,
mle: Number of memory limit exceeded verdicts,
wa: Number of wrong answer verdicts,
pe: Number of presentation error verdicts,
ac: Number of accepted verdicts,
rtl: Problem Run-Time limit,
status: Problem Status (0 = unavailable, 1 = normal, 2 = special judge) ,
```

## get_submissions(u16 pid, u32 start, u32 end)

Returns a list containing the submissions to a certain problem in a certain timeframe. The start and end arguments are Unix timestamps. The list is made of Submission dictionaries, wich have the following data:

``` Text
sid: Submission id,
pid: Problem id,
ver: Verdict of the problem,
lan: Language ID (1=ANSI C, 2=Java, 3=C++, 4=Pascal, 5=C++11) ,
run: Runtime,
mem: Memory usage,
rank: Rank of the sumbission,
sbt: Submission time (in Unix timestamp),
name: Name of the user,
uname: Username of the user
```

## get_user_submissions(u32 uid, u16 count)

Returns the user's last `count` submissions to any problem. Returns an UserSubmission dictionary which contain the following data:

``` Text
name: Name of the user,
uname: Username of the user,
subs: List of lists containing the submission data. This data is:

    Submission ID
    Problem ID
    Verdict ID
    Runtime
    Submission Time (unix timestamp)
    Language ID (1=ANSI C, 2=Java, 3=C++, 4=Pascal, 5=C++11)
    Submission Rank 
```

## get_usubs_problem(u32 uid, u16 pid, u16 count)

Returns a dictionary containing the last `count` submissions the speccified user to the selected problem. This dictionary contains `uid - UserSubmission` pairs, being the fields of UserSubmission:

``` Text
name: Name of the user,
uname: Username of the user,
subs: List of lists containing the submission data. This data is:

    Submission ID
    Problem ID
    Verdict ID
    Runtime
    Submission Time (unix timestamp)
    Language ID (1=ANSI C, 2=Java, 3=C++, 4=Pascal, 5=C++11)
    Submission Rank 
```

## get_ranking(u32 uid, u16 above, u16 below)

Returns a list containing the `above` and `below` users from user `uid` in the ranking. This list is made of UserRank dictionaries, which contain the following information:

``` Text
rank: Rank of the user,
old: Non zero if the user is an old UVa user that hasn't migrate ,
userid: Id of the user,
name: Name of the user,
username: Username of the user,
ac: Number of accepted verdicts,
nos: Number of submissions,
activity: List containing the activity of the user for the last 2 days, 7 days, 31 days, 3 months, and 1 year respectively.
```

## get_uid(String uname)

Returns the user id from its username. Usefull to get the id and use it in subsequent calls to the API

## get_pdf_url(String num)

Returns the URL to a certain problem's pdf.
