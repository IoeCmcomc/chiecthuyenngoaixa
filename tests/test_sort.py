import pytest
import random

from ctnx.sort import ViCollator, vi_sort_key
from ctnx.legacy import ViSortKey
from ctnx import num_to_words


def generate_vi_data(num_entries=10, title_rate=0.5):
    family_names = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý",
                    "Hoàng Phủ", "Sùng", "Vừ", "Giàng", "Lại", "Ông", "Ốc", "Trương", "Nghịch", "Nguyến", "Nguyền", "Nguyển", "Nguyện",
                    "Tô", "Trịnh"]
    middle_names = ["Văn", "Thị", "Hữu", "Đức", "Thành", "Ngọc", "Minh", "Quang", "Xuân", "Thu", "Hải", "Diệu", "Thanh", "Mạnh",
                    "Gia", "Tuấn", "Như", "Thì", "Hài", "Hái", "Bảo", "Quốc"]
    given_names = ["An", "Bình", "Châu", "Dũng", "Giang", "Hà", "Hai", "Hải", "Hoàng", "Khánh", "Lan", "Minh", "Nam", "Nghĩa",
                   "Phong", "Quân", "Sơn", "Tâm", "Thảo", "Trang", "Uyên", "Vinh", "Yến", "Anh", "Bân", "Cuội", "Hiền", "Linh",
                   "Ngân", "Phú", "Quyên", "Quỳnh", "Tính", "Tình", "Thành", "Trâm", "Trầm", "Cường", "Liên", "Nhân", "My", "Trà",
                   "Cúc", "Hùng", "Thiện",]

    verbs = ["khóc", "cười", "đi", "chạy", "ngủ", "hát", "suy tư", "nhớ", "quên", "kiếm tìm", "chờ đợi", "biến mất", "quay về",
             "lập trình", "học", "ngã", "hỏi", "rút lui", "tu luyện", "tập luyện", "tiếp tục", "từ bỏ", "hi vọng",
             "nấu nướng"]
    transitive_verbs = ["yêu", "ghét", "nhớ", "tìm", "ngắm", "viết", "đọc", "vẽ", "gọi", "giữ", "buông", "xử lí", "huấn luyện",
                        "trốn", "truy đuổi", "giải mã", "vun đắp", "chụp", "quên", "nghiện", "nhờ", "theo đuổi", "kể về",
                        "thao túng", "thôi miên", "tiêu diệt", "phát hiện", "bắt", "quấn lấy"]
    adjectives = ["buồn", "vui", "đẹp", "xanh", "đỏ", "tím", "vàng", "hồng", "trắng", "đen", "đắt giá", "xa xôi", "lặng lẽ",
                  "ồn ào", "rực rỡ", "lạnh lùng", "ấm áp", "mong manh", "hoang hoải", "uê oải", "thiết tha", "nhị phân",
                  "da diêt", "bồi hồi", "mát mẻ", "chói chang", "ánh ỏi", "óng ánh", "ngốc nghếch", "hiền hoà", "đáng yêu",
                  "tiễn táng", "chậm chạp", "nhanh nhẹn"]
    subjects = ["anh", "em", "người ấy", "chúng ta", "cô gái", "chàng trai", "họ", "kẻ lạ mặt", "gió", "nắng", "mây", "tin tặc",
                "người đàn bà", "người nghệ sĩ nhiếp ảnh", "chánh án", "chúa tể", "linh hồn", "hoàng tử", "công chúa", "hốc trưởng",
                "cầu thủ", "kì thủ", "tuyển thủ", "nữ sinh", "nam sinh", "cô giáo", "thầy giáo", "siêu nhân", "đội trưởng", "tổ đội",
                "thiên thần", "ác quỷ"]
    objects = subjects + ["bài thơ", "bức tranh", "quá khứ", "tương lai", "bí mật", "câu chuyện", "phép thuật", "chiếc thuyền", "cây đàn bầu",
                          "cây chổi", "lẩu thái", "bát phở", "trà sữa", "chiếc thuyền ngoài xa",]
    locations = ["lối nhỏ", "quán cũ", "cuối phố", "trong mơ", "dưới mưa", "bên hiên nhà", "trên đồi", "ngôi trường", "thế giới khác",
                 "quán phở", "đại lộ", "sân bay", "rạp xiếc", "thành phố", "thị trấn", "ngã tư", "lễ hội", "bản làng", "sân khấu"]
    time_words = ["hôm qua", "hôm nay", "ngày mai", "mùa xuân", "mùa hè", "mùa thu", "mùa đông", "thanh xuân này", "tuổi trẻ này",
                  "đêm nay", "ngày ấy", "thu cuối", "sau này", "năm ấy", "giây phút đó"]
    frequencies = ["hay", "thường", "luôn", "thi thoảng",
                   "đôi khi", "chợt", "hiếm khi", "lúc nào cũng"]
    units = ["giây", "phút", "giờ", "ngày", "tháng", "năm", "thế kỉ"]
    tenses = ["đã", "sẽ", "vừa"]
    nouns = locations + time_words + [
        "giấc mơ", "kỉ niệm", "bầu trời", "con đường", "dòng sông", "ngôi nhà",
        "tình yêu", "nỗi nhớ", "cà phê", "cuốn sách", "cơn mưa", "khuôn mặt", "ngôn ngữ", "thư viện",
        "chương trình", "ác mộng", "hồi ức", "điện thoại", "khế ước", "cây khế", "khỉ đầu chó",
        "vòng xoáy", "thời trang", "nhật kí", "hoài bão", "căn bệnh", "hội đồng", "vũ trụ", "dân ca", "tiểu thuyết",
        "ban nhạc", "bản nhạc", "mặt nạ", "vai diễn", "cảm xúc", "âm vị", "ngữ đoạn"]

    def get_full_name():
        family_name = random.choice(family_names)

        while True:
            first_given_name = random.choice(given_names)
            if first_given_name != family_name:
                break

        middles = []
        num_middles = 1 if random.random() < 0.6 else 2

        filtered_middles = [m for m in middle_names if m !=
                            family_name and m != first_given_name]

        if len(filtered_middles) >= num_middles:
            middles = random.sample(filtered_middles, num_middles)
        else:
            middles = filtered_middles

        return f"{family_name} {' '.join(middles)} {first_given_name}"

    def get_title():
        pattern_type = random.randint(1, 13)

        if pattern_type == 1:  # <danh từ>, <danh từ> và <danh từ>
            return f"{random.choice(nouns)}, {random.choice(nouns)} và {random.choice(nouns)}".capitalize()
        elif pattern_type == 2:  # <danh từ> của <họ tên>
            return f"{random.choice(nouns).capitalize()} của {get_full_name()}"
        elif pattern_type == 3:  # <chủ ngữ> <hành động>, <chủ ngữ> <hành động>
            return f"{random.choice(subjects)} {random.choice(verbs)}, {random.choice(subjects)} {random.choice(verbs)}".capitalize()
        elif pattern_type == 4:  # <số> (giây|phút|ngày|năm) <hành động>
            return f"{num_to_words(random.randint(1, 100))} {random.choice(units)} {random.choice(verbs)}".capitalize()
        # <từ chỉ thời gian> này, <chủ ngữ> (đã|sẽ) <hành động>
        elif pattern_type == 5:
            return f"{random.choice(time_words)}, {random.choice(subjects)} {random.choice(tenses)} {random.choice(verbs)}".capitalize()
        elif pattern_type == 6:  # <đối tượng> <tính từ> <từ chỉ tần suất> lại <hành động> tôi
            return f"{random.choice(objects)} {random.choice(adjectives)} {random.choice(frequencies)} lại {random.choice(transitive_verbs)} tôi".capitalize()
        elif pattern_type == 7:  # <ngoại động từ> <đối tượng> ở <địa điểm>
            return f"{random.choice(transitive_verbs)} {random.choice(objects)} ở {random.choice(locations)}".capitalize()
        elif pattern_type == 8:  # <ngoại động từ> <đối tượng>, tôi <động từ> <đối tượng> lúc nào không hay
            return f"{random.choice(transitive_verbs)} {random.choice(objects)}, tôi {random.choice(transitive_verbs)} {random.choice(objects)} lúc nào không hay".capitalize()
        elif pattern_type == 9:  # <danh từ> <tính từ>
            return f"{random.choice(nouns)} {random.choice(adjectives)}".capitalize()
        elif pattern_type == 10:  # <từ chỉ thời gian> là <danh từ> của <đối tượng>
            return f"{random.choice(time_words)} là {random.choice(nouns)} của {random.choice(objects)}".capitalize()
        elif pattern_type == 11:  # Tại <địa điểm>, <chủ ngữ> <hành động>
            return f"Tại {random.choice(locations)}, {random.choice(subjects)} {random.choice(verbs)}"
        elif pattern_type == 12:  # <danh từ> hay <danh từ>
            return f"{random.choice(nouns)} hay {random.choice(nouns)}".capitalize()
        else:
            return f"Câu chuyện của {get_full_name()} và {get_full_name()}"

    results = []
    for _ in range(num_entries):
        if random.random() > title_rate:
            results.append(get_full_name())
        else:
            results.append(get_title())

    return results


@pytest.fixture
def dataset():
    random.seed(67)

    data = generate_vi_data(50000, 0.5)
    # print(data)
    return data


def test_bench_naive_sort(benchmark, dataset):
    result = benchmark(sorted, dataset)
    assert len(result) == len(dataset)


def test_bench_ViSortKey(benchmark, dataset):
    result = benchmark(sorted, dataset, key=ViSortKey)
    assert len(result) == len(dataset)


def test_bench_ViCollator(benchmark, dataset):
    result = benchmark(sorted, dataset, key=vi_sort_key)
    assert len(result) == len(dataset)


def test_compare_old_algo():
    small_sample = ["đá", "dạ", "đa", "da", "dà", "dá", "dã", "đà", "đã",
                    "đả", "dả", "đạ", "đàn", "đan", "đán", "đản", "đãn", "đạn", "đa đa"]
    random.shuffle(small_sample)

    collator = ViCollator(('', '\\', '/', '?', '~', '.'))

    results = []
    results.append(sorted(small_sample))
    results.append(sorted(small_sample, key=ViSortKey))
    results.append(sorted(small_sample, key=collator.key))

    print(f"Original:       {results.pop(0)}")
    print(f"ViSortKey:      {results.pop(0)}")
    print(f"ViCollator.key: {results.pop(0)}")


def test_custom_tone_order():
    list = ['mèo', 'méo', 'meo', 'mẹo', 'mẻo', 'mẽo', 'dán', 'đan']

    collator = ViCollator(('', '.', '~', '?', '\\', '/'))
    sorted_list = sorted(list, key=collator.key)
    assert sorted_list == ['dán', 'đan', 'meo',
                           'mẹo', 'mẽo', 'mẻo', 'mèo', 'méo']
