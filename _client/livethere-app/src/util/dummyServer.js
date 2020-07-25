export async function dummyFetchPopupItems(keyword){
    if (!keyword || keyword === '') {
        return null;
    }
    return [`Search with Key ${keyword}`, 'Dummy Search 1', 'Dummy Search 2', 'Dummy Search 3', 'Dummy Search 4'];
}
