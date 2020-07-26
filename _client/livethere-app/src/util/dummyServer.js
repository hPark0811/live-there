export async function dummyFetchPopupItems(keyword){
    if (!keyword || keyword === '') {
        return null;
    }
    return [`Search with Key ${keyword}`, 'Dummy search 1', 'Dummy search 2', 'Dummy search 3', 'Dummy search 4'];
}
