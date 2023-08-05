//! Module containing different get request to the uHunt API
//! 
//! The requests are used to get certain data and are always organized into structs (or collections of a struct).
//! This API request get data from the Universidad de Valladolid competitive programming judge.
//! 
//! This library can be used both in Rust and in python, as building it with `maturin develop` creates a python 
//! module.
//! 

use std::collections::HashMap;

use cpython::{PyResult, Python, py_module_initializer, py_fn, ToPyObject, PyDict};
use reqwest::Url;
use exitfailure::ExitFailure;
use serde_derive::{Deserialize, Serialize};

/// A struct holding the data asociated with a problem
#[derive(Serialize, Deserialize, Debug)]
struct Problem {
    pid: u16,
    num: u16,
    title: String,
    dacu: u32,
    mrun: u64,
    mmem: u64,
    nover: u16,
    sube: u16,
    noj: u16,
    inq: u16,
    ce: u16,
    rf: u16,
    re: u16,
    ole: u16,
    tle: u16,
    mle: u16,
    wa: u16,
    pe: u16,
    ac: u16,
    rtl: u16,
    status: u8,
    rej: i32,
}

#[doc(hidden)]
impl ToPyObject for Problem {
    type ObjectType = PyDict;
    
    /// Conversion of a Problem struct into a Python dictionary
    fn to_py_object(&self, py: Python) -> PyDict {
        let dict = PyDict::new(py);

        dict.set_item(py, "pid", self.pid).unwrap();
        dict.set_item(py, "num", self.num).unwrap();
        dict.set_item(py, "title", self.title.to_py_object(py)).unwrap();
        dict.set_item(py, "dacu", self.dacu).unwrap();
        dict.set_item(py, "mrun", self.mrun).unwrap();
        dict.set_item(py, "mmem", self.mmem).unwrap();
        dict.set_item(py, "nover", self.nover).unwrap();
        dict.set_item(py, "sube", self.sube).unwrap();
        dict.set_item(py, "noj", self.noj).unwrap();
        dict.set_item(py, "inq", self.inq).unwrap();
        dict.set_item(py, "ce", self.ce).unwrap();
        dict.set_item(py, "rf", self.rf).unwrap();
        dict.set_item(py, "re", self.re).unwrap();
        dict.set_item(py, "ole", self.ole).unwrap();
        dict.set_item(py, "tle", self.tle).unwrap();
        dict.set_item(py, "mle", self.mle).unwrap();
        dict.set_item(py, "wa", self.wa).unwrap();
        dict.set_item(py, "pe", self.pe).unwrap();
        dict.set_item(py, "ac", self.ac).unwrap();
        dict.set_item(py, "rtl", self.rtl).unwrap();
        dict.set_item(py, "status", self.status).unwrap();
        dict.set_item(py, "rej", self.rej).unwrap();

        dict
    }
}

/// A Struct holding data for a problem submission
#[derive(Serialize, Deserialize, Debug)]
struct Submission {
    sid: i64,
    pid: u16,
    ver: u16,
    lan: u8,
    run: u64,
    mem: u64,
    rank: u16,
    sbt: u64,
    name: String,
    uname: String
}

#[doc(hidden)]
impl ToPyObject for Submission {
    type ObjectType = PyDict;

    /// Conversion of a Submission struct into a Python dictionary
    fn to_py_object(&self, py: Python) -> PyDict {
        let dict = PyDict::new(py);

        dict.set_item(py, "sid", self.sid).unwrap();
        dict.set_item(py, "pid", self.pid).unwrap();
        dict.set_item(py, "ver", self.ver).unwrap();
        dict.set_item(py, "lan", self.lan).unwrap();
        dict.set_item(py, "run", self.run).unwrap();
        dict.set_item(py, "mem", self.mem).unwrap();
        dict.set_item(py, "rank", self.rank).unwrap();
        dict.set_item(py, "sbt", self.sbt).unwrap();
        dict.set_item(py, "name", self.name.to_py_object(py)).unwrap();
        dict.set_item(py, "uname", self.uname.to_py_object(py)).unwrap();

        dict
    }
}

/// A struct holding data for an user's submissions
#[derive(Serialize, Deserialize, Debug, PartialEq)]
struct UserSubmission {
    name: String,
    uname: String,
    subs: Vec<Vec<i64>>
}

#[doc(hidden)]
impl ToPyObject for UserSubmission {
    type ObjectType = PyDict;

    /// Conversiom of a UserSubmission struct into a Python dictionary
    fn to_py_object(&self, py: Python) -> PyDict {
        let dict = PyDict::new(py);
        
        dict.set_item(py, "name", self.name.to_py_object(py)).unwrap();
        dict.set_item(py, "uname", self.uname.to_py_object(py)).unwrap();
        dict.set_item(py, "subs", self.subs.to_py_object(py)).unwrap();
        
        dict
    }
}

/// A struct holding data for the position in the ranking of a user
#[derive(Serialize, Deserialize, Debug)]
struct UserRank {
    rank: u32,
    old: u8,
    userid: u32,
    name: String,
    username: String,
    ac: u16,
    nos: u16,
    activity: Vec<u16>
}

#[doc(hidden)]
impl ToPyObject for UserRank {
    type ObjectType = PyDict;

    /// COnversion of a UserRank into a Python dictionary
    fn to_py_object(&self, py: Python) -> PyDict {
        let dict = PyDict::new(py);

        dict.set_item(py, "rank", self.rank).unwrap();
        dict.set_item(py, "old", self.old).unwrap();
        dict.set_item(py, "userid", self.userid).unwrap();
        dict.set_item(py, "name", self.name.to_py_object(py)).unwrap();
        dict.set_item(py, "username", self.username.to_py_object(py)).unwrap();
        dict.set_item(py, "ac", self.ac).unwrap();
        dict.set_item(py, "nos", self.nos).unwrap();
        dict.set_item(py, "activity", self.activity.to_py_object(py)).unwrap();

        dict
    }
}

py_module_initializer!(u_interface, |py, m| {
    m.add(py, "__doc__", "Python module written in Rust to make requests to uHunt's API")?;
    m.add(py, "get_problem", py_fn!(py, get_problem_py(num: u16)))?;
    m.add(py, "get_problem_pid", py_fn!(py, get_problem_by_pid_py(pid: u16)))?;
    m.add(py, "get_submissions", py_fn!(py, get_submissions_py(pid: u16, start: u32, end: u32)))?;
    m.add(py, "get_user_submissions", py_fn!(py, get_user_subs_py(uid: u32, count: u16)))?;
    m.add(py, "get_usubs_problem", py_fn!(py, get_user_subs_to_problem_py(uid: u32, pid: u16, count: u16)))?;
    m.add(py, "get_ranking", py_fn!(py, get_ranking_py(uid: u32, above: u16, below: u16)))?;
    m.add(py, "get_uid", py_fn!(py, get_uid_py(uname: String)))?;
    m.add(py, "get_pdf_url", py_fn!(py, get_pdf_url_py(num: String)))?;
    Ok(())
});

/// Returns the problem with number `num`, or an empty struct if it
/// does not exist. This function is async, that means it has to be
/// called inside an async function/method or using `tokio::Runtime.block_on()`.
/// 
/// # Arguments
/// 
/// * `num` - An unsigned, 16 bit number indicating the number of the
/// problem.
/// 
/// # Examples 
/// 
/// ```
/// // Returns the 462nd problem
/// let problem: Problem = get_problem(462).await?;
/// ```
/// 
async fn get_problem(num: u16) -> Result<Problem, ExitFailure> {
    let url = format!(
        "https://uhunt.onlinejudge.org/api/p/num/{}",
        num
    );

    let url = Url::parse(&*url)?;
    let prob = reqwest::get(url).await?.json::<Problem>().await?;

    Ok(prob)
}


/// Returns the problem with id `pid`, or an empty struct if it does
/// not exist. This function is async, that means it has to be
/// called inside an async function/method or using `tokio::Runtime.block_on()`.
/// 
/// # Arguments
/// 
/// * `pid` - An unsigned, 16 bit number indicating the id of the problem.
/// 
/// # Examples
/// 
/// ```
/// // Returns the problem with id 403
/// let problem: Problem = get_problem_by_pid(403).await?;
/// ```
/// 
async fn get_problem_by_pid(pid: u16) -> Result<Problem, ExitFailure> {
    let url = format!(
        "https://uhunt.onlinejudge.org/api/p/id/{pid}",
    );

    let url = Url::parse(&*url)?;
    let prob = reqwest::get(url).await?.json::<Problem>().await?;

    Ok(prob)
}

/// Returns a vector containing the submissions to a certain problem in 
/// a certain timeframe. This function is async, that means it has to be 
/// called inside an async function/method or using `tokio::Runtime.block_on()`.
/// 
/// # Arguments
/// 
/// * `pid` - An unsigned, 16 bit number indicating the id of the problem.
/// * `start` - An unsigned, 32 bit number indicating the start of the timeframe,
/// stated in Unix timestamp.
/// * `end` - An unsigned, 32 bit number indicating the end of the timeframe,
/// stated in Unix timestamp.
/// 
/// # Examples
/// 
/// ```
/// // Returns the submisions to problem with id 403, from 01/01/2023 - 12:00 to
/// // 01/02/2023 - 12:00
/// let sub: Vec<Submission> = get_submissions_problem(403, 1672531200, 1675209600).await?;
/// ```
/// 
async fn get_submissions_problem(pid: u16, start:u32, end: u32) -> Result<Vec<Submission>, ExitFailure> {
    let url = format!(
        "https://uhunt.onlinejudge.org/api/p/rank/{pid}/{start}/{end}",
    );

    let url = Url::parse(&*url)?;
    let sub = reqwest::get(url).await?.json::<Vec<Submission>>().await?;

    Ok(sub)
}

/// Returns the user's last submissions to any problem. This function is async, 
/// that means it has to be called inside an async function/method or using 
/// `tokio::Runtime.block_on()`.
/// 
/// # Arguments
/// 
/// * `uid` - An unsigned, 32 bit number indicating the id of the user
/// * `count` - An unsigned, 16 bit number indicating the number of submissions.
/// to show. Note this number is capped at 100 and will return an error if.
/// it is more than this.
/// 
/// # Examples
/// 
/// ```
/// // Returns the last 5 submissions of user LovetheFrogs
/// let user_subs: UserSubmission = get_user_submissions(1589052, 5).await?;
/// ```
/// 
async fn get_user_submissions(uid: u32, count: u16) -> Result<UserSubmission, ExitFailure> {
    let url = format!(
        "https://uhunt.onlinejudge.org/api/subs-user-last/{uid}/{count}"
    );

    let url = Url::parse(&*url)?;
    let usubs = reqwest::get(url).await?.json::<UserSubmission>().await?;

    Ok(usubs)
}

/// Returns a HashMap containing the submissions the speccified user to 
/// the selected problem. This function is async, that means it has to be called 
/// inside an async function/method or using `tokio::Runtime.block_on()`.
/// 
/// # Arguments
/// 
/// * `uid` - An unsigned, 32 bit number indicating the id of the user.
/// * `pid` - An unsigned, 16 bit number indicating the id of the problem.
/// * `count` - An unsigned, 16 bit number indicating the number of submissions.
/// to show. Note this number is capped at 100 and will return an error if.
/// it is more than this.
/// 
/// # Examples
/// 
/// ```
/// // Return the last 5 submissions of user LovetheFrogs to problem with id
/// // 403.
/// let usubs_prob: HashMap<u32, UserSubmission> = get_usubmissions_to_problem(1589052, 403,5).await?;
/// ```
/// 
async fn get_usubmissions_to_problem(uid: u32, pid: u16, count: u16) -> Result<HashMap<u32, UserSubmission>, ExitFailure> {
    let url = format!(
        "https://uhunt.onlinejudge.org/api/subs-pids/{uid}/{pid}/{count}"
    );

    let url = Url::parse(&*url)?;
    let usubs = reqwest::get(url).await?.json::<HashMap<u32, UserSubmission>>().await?;

    Ok(usubs)
}

/// Returns a Vector containing the Rank of the `above` users over the user 
/// with id `uid`, the user with that id and the `below` users, below the
/// asme user. This function is async, that means it has to be called 
/// inside an async function/method or using `tokio::Runtime.block_on()`.
/// 
/// # Arguments
/// 
/// * `uid` - An unsigned, 32 bit number indicating the id of the user.
/// * `above` - An unsigned, 16 bit number indicating the number of users
/// to show above user wit id `pid`.
/// * `below` - An unsigned, 16 bit number indicating the number of users
/// to show below user wit id `pid`.
/// 
/// # Examples
/// 
/// ```
/// // Return the 2 users' rankings above and below the user LovetheFrogs
/// let uranking: Vec<UserRank> = get_ranking(1589052, 2, 2).await?;
/// ```
/// 
async fn get_ranking(uid: u32, above: u16, below: u16) -> Result<Vec<UserRank>, ExitFailure> {
    let url = format!(
        "https://uhunt.onlinejudge.org/api/ranklist/{uid}/{above}/{below}"
    );

    let url = Url::parse(&*url)?;
    let rank = reqwest::get(url).await?.json::<Vec<UserRank>>().await?;

    Ok(rank)
}

/// Returns the user's id number by searching using the stated username.
/// This function is async, that means it has to be called inside an async 
/// function/method or using `tokio::Runtime.block_on()`.
/// 
/// # Arguments
/// 
/// * `uname` - A String that is the username of the user whose id we want to
/// obtain
/// 
/// # Examples
/// 
/// ```
/// // Get the id of the user "LovetheFrogs"
/// let uid: u32 = get_uid_from_uname(String::from("LovetheFrogs")).await?;
/// ```
/// 
async fn get_uid_from_uname(uname: String) -> Result<u32, ExitFailure> {
    let url = format!(
        "https://uhunt.onlinejudge.org/api/uname2uid/{uname}"
    );

    let url = Url::parse(&*url)?;
    let uid = reqwest::get(url).await?.json::<u32>().await?;

    Ok(uid)
}

/// Returns the URL of a pdf for a certain problem number.
/// 
/// # Arguments
/// 
/// * `num` - A String containing the number of the problem. A String is 
/// used instead of an u16 so operations with its contents can be done easier.
/// 
/// # Examples
/// 
/// ```
/// // Get the URL of the pdf for the problem 462
/// let url: String = get_pdf_from_problem(String::from("462"));
/// ```
/// 
fn get_pdf_url_from_problem(num: String) -> String {
    let prelude = match num.len() {
        3 => &num[..1],
        4 => &num[..2],
        5 => &num[..3],
        _ => &num[..3],
    };

    format!("https://onlinejudge.org/external/{prelude}/{num}.pdf")

}

#[doc(hidden)]
fn get_problem_py(_: Python<'_>, num: u16) -> PyResult<Problem> {
    let rt = tokio::runtime::Runtime::new().unwrap();
    let contents = rt.block_on(get_problem(num)).unwrap();

    Ok(contents)
}

#[doc(hidden)]
fn get_problem_by_pid_py(_: Python<'_>, pid: u16) -> PyResult<Problem> {
    let rt = tokio::runtime::Runtime::new().unwrap();
    let contents = rt.block_on(get_problem_by_pid(pid)).unwrap();

    Ok(contents)
}

#[doc(hidden)]
fn get_submissions_py(_: Python<'_>, pid: u16, start: u32, end: u32) -> PyResult<Vec<Submission>> {
    let rt = tokio::runtime::Runtime::new().unwrap();
    let contents = rt.block_on(get_submissions_problem(pid, start, end)).unwrap();
    
    Ok(contents)
}

#[doc(hidden)]
fn get_user_subs_py(_: Python<'_>, uid: u32, count: u16) -> PyResult<UserSubmission> {
    let rt = tokio::runtime::Runtime::new().unwrap();
    let contents = rt.block_on(get_user_submissions(uid, count)).unwrap();
    
    Ok(contents)
}

#[doc(hidden)]
fn get_user_subs_to_problem_py(_: Python<'_>, uid: u32, pid: u16, count: u16) -> PyResult<HashMap<u32, UserSubmission>> {
    let rt = tokio::runtime::Runtime::new().unwrap();
    let contents = rt.block_on(get_usubmissions_to_problem(uid, pid, count)).unwrap();

    Ok(contents)
}

#[doc(hidden)]
fn get_ranking_py(_: Python<'_>, uid: u32, above: u16, below: u16) -> PyResult<Vec<UserRank>> {
    let rt = tokio::runtime::Runtime::new().unwrap();
    let contents = rt.block_on(get_ranking(uid, above, below)).unwrap();
    
    Ok(contents)
}

#[doc(hidden)]
fn get_uid_py(_: Python<'_>, uname: String) -> PyResult<u32> {
    let rt = tokio::runtime::Runtime::new().unwrap();
    let contents = rt.block_on(get_uid_from_uname(uname)).unwrap();
    
    Ok(contents)
}

#[doc(hidden)]
fn get_pdf_url_py(_: Python, num: String) -> PyResult<String> {
    Ok(get_pdf_url_from_problem(num))
}


#[cfg(test)]
mod tests {
    use super::*;
    use actix_rt::test;

    #[actix_rt::test]
    async fn test_get_a_problem() {
        let prob_462: Problem = get_problem(462).await.unwrap();
        assert_eq!(prob_462.pid, 403)
    }

    #[actix_rt::test]
    async fn test_get_problem_by_pid() {
        let prob_462: Problem = get_problem_by_pid(403).await.unwrap();
        assert_eq!(prob_462.num, 462)
    }

    #[actix_rt::test]
    async fn test_get_submissions() {
        let subs: Vec<Submission> = get_submissions_problem(403, 1, 2).await.unwrap();
        assert_eq!(subs[0].sid, 1065763);
    }

    #[actix_rt::test]
    async fn test_user_submissions() {
        let subs: UserSubmission = get_user_submissions(1589052, 1).await.unwrap();
        let vec: Vec<Vec<i64>> = vec![vec![28344490, 1587, 90, 360, 1680048279, 2, 3052]];
        let expected = UserSubmission {
            name: String::from("Marcos"),
            uname: String::from("LovetheFrogs"),
            subs: vec,
        };

        assert_eq!(expected, subs);
    }

    #[actix_rt::test]
    async fn test_usubmissions_to_problem() {
        let uid: u32 = 1589052;
        let subs = get_usubmissions_to_problem(uid, 403, 5).await.unwrap();

        let prob = subs.get(&uid).unwrap();

        assert_eq!(prob.uname, "LovetheFrogs")
    }

    #[actix_rt::test]
    async fn test_get_ranking() {
        let rank = get_ranking(1589052, 1, 1).await.unwrap();
        assert_eq!(rank[0].name, String::from("abigail"));
    }

    #[actix_rt::test]
    async fn test_uid_from_uname() {
        assert_eq!(get_uid_from_uname(String::from("LovetheFrogs")).await.unwrap(), 1589052);
    }

    #[test]
    async fn test_get_pdf_url() {
        assert_eq!(get_pdf_url_from_problem(String::from("462")), String::from("https://onlinejudge.org/external/4/462.pdf"));
    }
}