import streamlit as st
import requests
from urllib.parse import urlparse

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="URL Shortener", page_icon="")
st.title(" URL Shortener")

tab1, tab2 = st.tabs(["Shorten URL", "View Stats"])

with tab1:
    st.subheader("Create a short URL")

    with st.form("shorten_form"):
        long_url = st.text_input("Enter the long URL (with http/https)")
        col1, col2 = st.columns(2)

        with col1:
            expires_in_minutes = st.number_input(
                "Expiry (minutes, optional)", min_value=0, step=5, value=0
            )
        with col2:
            custom_alias = st.text_input(
                "Custom alias (optional, e.g. my-link)"
            )

        submitted = st.form_submit_button("Shorten")

    if submitted:
        if not long_url:
            st.error("Please enter a URL")
        #  basic format check before calling backend
        elif not long_url.startswith(("http://", "https://")):
            st.error(" Invalid URL format. Kindly check again!")
        else:
            payload = {
                "long_url": long_url,
                "expires_in_seconds": int(expires_in_minutes * 60)
                if expires_in_minutes > 0
                else None,
                "custom_alias": custom_alias or None,
            }
            try:
                res = requests.post(
                    f"{API_BASE}/api/shorten", json=payload, timeout=5
                )
                if res.status_code == 200:
                    data = res.json()
                    short_url = data["short_url"]
                    st.success("Short URL created!")
                    st.write("**Short URL:**")
                    st.code(short_url)
                    st.markdown(f"[ Open short URL]({short_url})")

                else:
                    try:
                        detail = res.json().get("detail", "Unknown error")
                        if isinstance(detail, list):
                            msgs = [
                                d.get("msg", "")
                                for d in detail
                                if isinstance(d, dict)
                            ]
                            if any("URL scheme" in m for m in msgs):
                                st.error(
                                    "Invalid URL format. Kindly check again!"
                                )
                            else:
                                st.error(
                                    "Invalid input. Please check your URL and try again."
                                )
                        else:
                            if "URL scheme" in str(detail):
                                st.error(
                                    "Invalid URL format. Kindly check again!"
                                )
                            else:
                                st.error(f" {detail}")
                    except Exception:
                        st.error(" Something went wrong. Please try again.")
            except Exception as e:
                st.error(f"Request failed: {e}")

with tab2:
    st.subheader("View statistics for a short URL")

    with st.form("stats_form"):
        input_code_or_url = st.text_input("Enter short code or full short URL")
        stats_submitted = st.form_submit_button("Get Stats")

    if stats_submitted:
        if not input_code_or_url:
            st.error("Please enter a value")
        else:
            parsed = urlparse(input_code_or_url)
            if parsed.scheme and parsed.netloc:
                short_code = parsed.path.lstrip("/")
            else:
                short_code = input_code_or_url.strip().replace("/", "")

            if not short_code:
                st.error("Invalid short code")
            else:
                try:
                    res = requests.get(
                        f"{API_BASE}/api/stats/{short_code}", timeout=5
                    )
                    if res.status_code == 200:
                        data = res.json()
                        st.write("**Long URL:**", data["long_url"])
                        st.write("**Short code:**", data["short_code"])
                        st.write("**Clicks:**", data["clicks"])
                        st.write("**Created at:**", data["created_at"])
                        st.write(
                            "**Expires at:**",
                            data["expires_at"] if data["expires_at"] else "No expiry",
                        )

                        short_url = f"{API_BASE}/{short_code}"
                        st.write("**Short URL:**")
                        st.code(short_url)
                        st.markdown(f"[ Open short URL]({short_url})")

                    else:
                        try:
                            detail = res.json().get("detail", "Not found")
                        except Exception:
                            detail = res.text
                        st.error(f"Error: {detail}")
                except Exception as e:
                    st.error(f"Request failed: {e}")
