import win32com.client as wc
import os


def get_file_metadata(path_p, filename_p, metadata_):
    sh = wc.gencache.EnsureDispatch('Shell.Application', 0)
    ns = sh.NameSpace(path_p)

    file_metadata = dict()
    item = ns.ParseName(str(filename_p))
    metadata = ['Name', 'Size', 'Item type', 'Date modified', 'Date created', 'Date accessed', 'Attributes',
                'Offline status', 'Availability', 'Perceived type', 'Owner', 'Kind', 'Date taken',
                'Contributing artists', 'Album', 'Year', 'Genre', 'Conductors', 'Tags', 'Rating', 'Authors',
                'Title',
                'Subject', 'Categories', 'Comments', 'Copyright', '#', 'Length', 'Bit rate', 'Protected',
                'Camera model', 'Dimensions', 'Camera maker', 'Company', 'File description', 'Masters keywords',
                'Masters keywords']
    for ind, attribute in enumerate(metadata):
        attr_value = ns.GetDetailsOf(item, ind)
        if attr_value:
            file_metadata[attribute] = attr_value
    ans = {}
    for x in range(len(metadata_)):
        ans[metadata_[x]] = file_metadata[metadata_[x]]
    return ans


def get_filenames(path_p, endings=['mp4']):
    filenames = [f for f in os.listdir(path_p) if os.path.isfile(os.path.join(path_p, f))]
    ans = []
    for i in range(len(filenames)):
        if filenames[i].split(".")[-1] in endings:
            ans.append(filenames[i])
    return ans
