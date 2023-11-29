# import requests

# def download_pdf(url, destination):
#     response = requests.get(url, verify=False)
#     if response.status_code == 200:
#         with open(destination, 'wb') as file:
#             file.write(response.content)
#         print(f"Downloaded PDF from {url} to {destination}")
#     else:
#         print(f"Failed to download PDF from {url}. Status code: {response.status_code}")

# # Example usage:
# pdf_url = "https://jad.shahroodut.ac.ir/data/jadm/news/copy.pdf"
# destination_path = "pdf_file/downloaded_file.pdf"

# download_pdf(pdf_url, destination_path)

# ...............................................................

# import requests
# def is_binary_content_pdf(content):
#     pdf_signature = b'%PDF'
#     return content.startswith(pdf_signature)

# # Example usage:
# url = 'https://www.toaan.gov.vn/webcenter/ShowProperty?nodeId=/UCMServer/TAND025648'
# response = requests.get(url, verify=False)

# if response.status_code == 200:
#     # Check if the content is a PDF
#     if is_binary_content_pdf(response.content):
#         print('The content is a PDF file.')
#     else:
#         print('The content is not a PDF file.')
# else:
#     print(f'Failed to fetch content. Status code: {response.status_code}')

# ..........................................................
import os

folder_path = "pdf_file/ui"  # Thay thế bằng đường dẫn thư mục mới bạn muốn tạo

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print("Thư mục mới đã được tạo.")
else:
    print("Thư mục đã tồn tại.")
