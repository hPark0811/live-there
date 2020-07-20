export function dummyFetchPopupItems(keyword){
    let promise = new Promise((resolve, reject)=>{
        resolve([`Search with Key${Math.random()}`, 'Dummy Search 1', 'Dummy Search 2', 'Dummy Search 3', 'Dummy Search 4']);
    })
    return promise;
};