import streamlit as st
import os

def get_image_size(file_path):
    """Get the size of an image in MB."""
    return os.path.getsize(file_path) / (1024 * 1024)

def read_image(file_path):
    """Read an image file."""
    with open(file_path, 'rb') as f:
        return f.read()

def write_image(file_path, data):
    """Write data to an image file."""
    with open(file_path, 'wb') as f:
        f.write(data)

def simulate_compression(image_data, quality):
    """Simulate compression by truncating the data."""
    truncated_length = int(len(image_data) * (quality / 100))
    return image_data[:truncated_length]

def optimize_image(image_data, quality):
    """Optimize the image by simulating compression."""
    return simulate_compression(image_data, quality)

def main():
    st.set_page_config(layout='wide')
    st.title("Image Optimizer")
    st.write("Upload an image to optimize its size.")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        temp_file_path = f"temp_{uploaded_file.name}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())

        original_size = get_image_size(temp_file_path)
        st.write(f"Original image size: {original_size:.2f} MB")

        st.image(temp_file_path, caption="Original Image", use_container_width=True)

        if original_size > 2:
            st.warning("Image is larger than 2MB. Let's optimize it.")

            qualities = [75, 50, 25]
            optimized_results = {}

            for quality in qualities:
                original_data = read_image(temp_file_path)
                optimized_data = optimize_image(original_data, quality)

                optimized_path = f"optimized_{quality}_{uploaded_file.name}"
                write_image(optimized_path, original_data)  

                optimized_results[quality] = {
                    "size": len(optimized_data) / (1024 * 1024), 
                    "data": optimized_data, 
                }

                st.write(f"**{quality}% Quality Preview (Simulated Size: {optimized_results[quality]['size']:.2f} MB)**")
                st.image(temp_file_path, caption=f"{quality}% Quality", use_container_width=True)

            chosen_quality = st.radio("Choose a quality level to download:", qualities, index=0)

            if chosen_quality:
                chosen_result = optimized_results[chosen_quality]
                st.write(f"Selected {chosen_quality}% Quality - Simulated Size: {chosen_result['size']:.2f} MB")

                st.download_button(
                    label=f"Download {chosen_quality}% Quality Image",
                    data=chosen_result['data'],
                    file_name=f"optimized_{chosen_quality}_{uploaded_file.name}",
                    mime="image/jpeg",
                )

        else:
            st.success("Image size is under 2MB. No optimization needed.")

if __name__ == "__main__":
    main()
